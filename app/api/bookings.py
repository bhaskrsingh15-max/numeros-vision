"""
BOOKINGS & CONSULTATION API — Consultation Enquiry & Booking
Handles: Enquiry-First Consultation Leads, Session Requests, Booking Confirmations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import hashlib, json, os, re

router = APIRouter(prefix="/api/v1/bookings", tags=["Bookings"])
consultation_router = APIRouter(prefix="/api/v1/consultation", tags=["Consultation"])

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ConsultationEnquiryRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, description="Full name of enquirer")
    email: str = Field(..., min_length=5, max_length=150, description="Email address")
    phone: Optional[str] = Field("", max_length=30, description="Phone or WhatsApp number if preferred")
    area_of_interest: str = Field(..., min_length=2, max_length=150, description="Topics of interest")
    description: Optional[str] = Field("", max_length=3000, description="Brief description of requirements")
    preferred_contact_method: Optional[str] = Field("Email", description="Preferred contact method: Email, WhatsApp, or Phone")
    consent: bool = Field(..., description="Consent to be contacted regarding the enquiry")


class ConsultationEnquiryResponse(BaseModel):
    status: str = "success"
    enquiry_id: str
    message: str



def send_enquiry_to_support_email(req: ConsultationEnquiryRequest, enquiry_id: str, ts: datetime):
    """Dispatches consultation enquiry details to support@numerosvision.com via SMTP if configured."""
    smtp_host = os.getenv("EMAIL_SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587").strip() or 587)
    smtp_user = os.getenv("EMAIL_SMTP_USER", "").strip()
    smtp_pass = os.getenv("EMAIL_SMTP_PASSWORD", "").strip()
    target_email = "support@numerosvision.com"

    if not smtp_host or not smtp_user or not smtp_pass:
        print(f"[ENQUIRY NOTIFICATION] Saved to data/consultation_enquiries.jsonl (SMTP unconfigured for {target_email}).")
        return

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"✦ New 1-on-1 Consultation Enquiry [{enquiry_id}]: {req.name}"
        msg["From"] = f"Numeros Vision Website <{smtp_user}>"
        msg["To"] = target_email
        msg["Reply-To"] = req.email

        html = f"""
        <html>
        <body style="font-family:Arial,sans-serif; line-height:1.6; color:#2C2218; padding:20px;">
          <h2 style="color:#16835B;">✦ New 1-on-1 Consultation Enquiry Received</h2>
          <p><strong>Enquiry Reference:</strong> <code>{enquiry_id}</code></p>
          <hr style="border:0; border-top:1px solid #C9A227; margin:15px 0;" />
          <p><strong>Client Name:</strong> {req.name}</p>
          <p><strong>Client Email:</strong> <a href="mailto:{req.email}">{req.email}</a></p>
          <p><strong>Phone / WhatsApp:</strong> {req.phone or 'Not provided'}</p>
          <p><strong>Area of Interest:</strong> {req.area_of_interest}</p>
          <p><strong>Preferred Contact Method:</strong> {req.preferred_contact_method or 'Email'}</p>
          <p><strong>Specific Topics / Description:</strong><br />{req.description or 'No additional notes provided.'}</p>
          <p><strong>Statutory Consent Confirmed:</strong> {'Yes' if req.consent else 'No'}</p>
          <p style="font-size:12px; color:#7A654D;">Received at {ts.isoformat()} via numerosvision.com/consultation/</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
            if smtp_port == 587:
                server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, target_email, msg.as_string())
        print(f"[ENQUIRY NOTIFICATION SUCCESS] Delivered enquiry {enquiry_id} to {target_email}")
    except Exception as e:
        print(f"[ENQUIRY NOTIFICATION ERROR] Could not dispatch to {target_email}: {e}")

def _process_consultation_enquiry(req: ConsultationEnquiryRequest, background_tasks: BackgroundTasks) -> ConsultationEnquiryResponse:
    if not req.consent:
        raise HTTPException(status_code=400, detail="Consent to be contacted is required to submit a consultation enquiry.")

    if not EMAIL_REGEX.match(req.email.strip()):
        raise HTTPException(status_code=400, detail="Invalid email address format.")

    ts = datetime.utcnow()
    raw = f"{req.email}{req.name}{ts.isoformat()}"
    enquiry_id = "ENQ-" + ts.strftime("%Y%m%d") + "-" + hashlib.sha256(raw.encode()).hexdigest()[:6].upper()

    # Immediately record the enquiry
    log_consultation_enquiry(enquiry_id, req, ts)
    background_tasks.add_task(send_enquiry_to_support_email, req, enquiry_id, ts)

    confirmation_msg = (
        "Thank you for your interest in a personal consultation with Numeros Vision.\n\n"
        "We have received your enquiry. We will review the topics you have shared and contact you "
        "to discuss your requirements, the consultation format, availability and applicable fee.\n\n"
        "Submitting this form does not confirm a booking or require payment."
    )

    return ConsultationEnquiryResponse(
        status="success",
        enquiry_id=enquiry_id,
        message=confirmation_msg
    )


@router.post("/enquiry", response_model=ConsultationEnquiryResponse)
def submit_consultation_enquiry_bookings(req: ConsultationEnquiryRequest, background_tasks: BackgroundTasks):
    """Submit an enquiry-first consultation lead (mounted on /api/v1/bookings/enquiry)."""
    return _process_consultation_enquiry(req, background_tasks)


@consultation_router.post("/enquiry", response_model=ConsultationEnquiryResponse)
def submit_consultation_enquiry_direct(req: ConsultationEnquiryRequest, background_tasks: BackgroundTasks):
    """Submit an enquiry-first consultation lead (mounted on /api/v1/consultation/enquiry)."""
    return _process_consultation_enquiry(req, background_tasks)


class BookingRequest(BaseModel):
    name: str = Field(..., description="Client full name")
    email: str = Field(..., description="Client email address")
    phone: str = Field(..., description="WhatsApp/phone number")
    session_type: str = Field(..., description="'phone' or 'video'")
    preferred_date: str = Field(..., description="Date YYYY-MM-DD")
    preferred_time: Optional[str] = Field("", description="Preferred time slot")
    focus_area: Optional[str] = Field("", description="What to focus on")
    dob: Optional[str] = Field("", description="Date of birth DD/MM/YYYY")


class BookingResponse(BaseModel):
    status: str
    booking_id: str
    session_type: str
    amount_inr: int
    message: str
    whatsapp_link: str
    payment_note: str


PRICING = {
    "phone": {"amount": 2499, "duration": "45 minutes"},
    "video": {"amount": 3999, "duration": "60 minutes"},
    "personal": {"amount": 11400, "duration": "90 minutes"},
}

# Your WhatsApp business number (update this)
WHATSAPP_NUMBER = "919999999999"  # Replace with your actual number


@router.post("/request", response_model=BookingResponse)
def request_consultation(req: BookingRequest, background_tasks: BackgroundTasks):
    """
    Submit a consultation booking request.
    Returns booking ID, pricing, and WhatsApp confirmation link.
    """
    if req.session_type not in PRICING:
        raise HTTPException(status_code=400, detail="session_type must be 'phone', 'video', or 'personal'")

    pricing = PRICING[req.session_type]

    # Generate unique booking ID
    raw = f"{req.email}{req.preferred_date}{req.session_type}{datetime.utcnow().isoformat()}"
    booking_id = "NV" + hashlib.sha256(raw.encode()).hexdigest()[:10].upper()

    # Build WhatsApp message
    if req.session_type == "personal":
        session_label = "1-on-1 Master Personal Session (90 min)"
    elif req.session_type == "video":
        session_label = "Video Call (60 min)"
    else:
        session_label = "Phone Call (45 min)"
    wa_message = (
        f"Hello! I'd like to book a numerology consultation.%0A%0A"
        f"Booking ID: {booking_id}%0A"
        f"Session: {session_label}%0A"
        f"Name: {req.name}%0A"
        f"Date: {req.preferred_date}{' at ' + req.preferred_time if req.preferred_time else ''}%0A"
        f"DOB: {req.dob if req.dob else 'Not provided'}%0A"
        f"Focus: {req.focus_area if req.focus_area else 'General reading'}%0A%0A"
        f"Amount: INR {pricing['amount']:,}"
    )
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_message}"

    # Background task: log booking (replace with DB write in production)
    background_tasks.add_task(log_booking, booking_id, req, pricing)

    return BookingResponse(
        status="requested",
        booking_id=booking_id,
        session_type=req.session_type,
        amount_inr=pricing["amount"],
        message=f"Your booking request {booking_id} has been received. We will confirm via WhatsApp within 2 hours.",
        whatsapp_link=whatsapp_link,
        payment_note="Payment link will be shared on WhatsApp after confirmation. UPI / Card / NetBanking accepted."
    )


@router.get("/slots")
def get_available_slots(date: Optional[str] = None):
    """
    Returns available time slots for booking.
    In production, connect this to your Google Calendar API.
    """
    # Simulated available slots — replace with Google Calendar API in production
    return {
        "status": "ok",
        "date": date or "any",
        "available_slots": [
            "09:00 AM", "11:00 AM", "01:00 PM",
            "03:00 PM", "05:00 PM", "07:00 PM"
        ],
        "note": "All times are IST (Indian Standard Time)"
    }


@router.get("/pricing")
def get_pricing():
    """Returns current consultation pricing."""
    return {
        "phone": {
            "amount_inr": 2499,
            "duration": "45 minutes",
            "includes": [
                "Personal numerological blueprint (6 systems)",
                "Career, love, or financial guidance",
                "Gemstone & remedy prescription",
                "WhatsApp follow-up summary"
            ]
        },
        "video": {
            "amount_inr": 3999,
            "duration": "60 minutes",
            "includes": [
                "Everything in Phone Session",
                "Live Lo Shu Grid visualization",
                "Annual timing roadmap",
                "Recorded session link (optional)"
            ]
        },
        "personal": {
            "amount_inr": 11400,
            "original_price_inr": 24000,
            "duration": "90 minutes",
            "includes": [
                "90-minute private 1-on-1 session with Master Numerologist",
                "Birth Epoch Verification & deep multi-system chart synthesis",
                "Custom hand-crafted remedy plan, yantra & gemstone prescription",
                "30-day direct priority WhatsApp guidance",
                "Comprehensive Deluxe Destiny Dossier PDF report"
            ]
        }
    }


def log_consultation_enquiry(enquiry_id: str, req: ConsultationEnquiryRequest, ts: datetime):
    """
    Log consultation interest enquiry safely to file (or DB).
    Follows DPDP 2023 compliance, captures user consent and inquiry topics.
    Zero pricing stored or implied.
    """
    log_entry = {
        "enquiry_id": enquiry_id,
        "timestamp": ts.isoformat(),
        "name": req.name,
        "email": req.email,
        "phone": req.phone or "",
        "area_of_interest": req.area_of_interest,
        "description": req.description or "",
        "preferred_contact_method": req.preferred_contact_method or "Email",
        "consent": req.consent,
        "status": "received"
    }
    try:
        log_path = os.path.join(os.path.dirname(__file__), "../../data/consultation_enquiries.jsonl")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"[CONSULTATION ENQUIRY LOG ERROR] {e}")


def log_booking(booking_id: str, req: BookingRequest, pricing: dict):
    """
    Log booking to file (replace with PostgreSQL / Neon DB write in production).
    Schema: bookings table in Neon PostgreSQL
    """
    log_entry = {
        "booking_id": booking_id,
        "timestamp": datetime.utcnow().isoformat(),
        "name": req.name,
        "email": req.email,
        "phone": req.phone,
        "session_type": req.session_type,
        "preferred_date": req.preferred_date,
        "preferred_time": req.preferred_time,
        "focus_area": req.focus_area,
        "amount_inr": pricing["amount"],
        "status": "pending"
    }
    try:
        import os
        log_path = os.path.join(os.path.dirname(__file__), "../../data/bookings.jsonl")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"[BOOKING LOG ERROR] {e}")
