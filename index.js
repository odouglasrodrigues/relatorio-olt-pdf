const pdf = require('html-pdf-node');
const fs = require('fs');



const options = { format: 'A4', path: 'teste.pdf', printBackground:true};

// const fileInHtml = { content: fs.readFileSync('data.html', 'utf8') };

const fileInHtml = { url:'file:///C:/Users/dougl/Desktop/Projetos/html-pdf/data.html'};

// pdf.create(fileInHtml, options).toFile('businesscard.pdf', function (err, res) {
//     if (err) return console.log(err);
//     console.log(res); // { filename: '/app/businesscard.pdf' }
// });

pdf.generatePdf(fileInHtml, options).then(pdfBuffer => {
    console.log("PDF Buffer:-", pdfBuffer);
});