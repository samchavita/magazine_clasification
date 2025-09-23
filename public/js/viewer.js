const urlParams = new URLSearchParams(window.location.search);
const file = urlParams.get('file');
const fullUrl = window.location.origin + file;

console.log("Loading PDF from:", fullUrl);
console.log("PDF file param:", file);
console.log("Full URL being used:", fullUrl);


const pdfjsLib = window['pdfjs-dist/build/pdf'];

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';


let tuples = [];

const container = document.getElementById('pdf-container');
const formContainer = document.getElementById('form-container');

pdfjsLib.getDocument(fullUrl).promise
    .then(pdf => {
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            pdf.getPage(pageNum).then(page => {
                const scale = 1.2;
                const viewport = page.getViewport({ scale });

                const canvas = document.createElement('canvas');
                canvas.width = viewport.width;
                canvas.height = viewport.height;
                canvas.style.cursor = "pointer";
                container.appendChild(canvas);

                const context = canvas.getContext('2d');
                page.render({ canvasContext: context, viewport });

                canvas.addEventListener('click', () => {
                    const title = prompt(`Enter title for sub-PDF starting at page ${pageNum}`);
                    if (title) {
                        tuples.push({ page: pageNum, title });
                        const p = document.createElement('p');
                        p.innerText = `Selected Page ${pageNum}: ${title}`;
                        formContainer.appendChild(p);
                    }
                });
            });
        }
    })
    .catch(err => {    
        console.error("Error loading PDF:", err);
        alert("Failed to load PDF: " + err.message);
    });

function submitData() {
    fetch('/submit-titles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tuples, file })
    }).then(res => res.json())
      .then(data => alert(data.message));
}
