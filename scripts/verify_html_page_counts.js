const fs = require('fs');

const html = fs.readFileSync('app/static/sample.html', 'utf-8');

// Extract generateFormat1Pages, generateFormat2Pages, generateFormat3Pages
// We can mock client and test
const client = {
  name: "Bhaskr Singh",
  dob: "1981-11-28",
  gender: "male",
  phone: "+91 9818418039"
};

console.log("Client:", client.name, client.dob);
console.log("sample.html size:", html.length);
