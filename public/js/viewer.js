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
                    const title = prompt(`Enter title @ pg. ${pageNum}:`);
                    const level = prompt(`Enter level:`, "1");
                    if (title) {
                        tuples.push({ page: pageNum, title, level });
                        const p = document.createElement('p');
                        p.innerText = `Page ${pageNum}: ${title} (lv: ${level})`;
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
    // deactivate button
    const send_button = document.getElementById("send_data_button")
    send_button.disabled = true;


    // fetch('/submit-titles', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ tuples, file })
    // }).then(res => res.json())
    //   .then(data => alert(data.message));


    // const form = document.createElement('form');
    // form.method = 'POST';
    // form.action = '/submit-titles';

    // const data = { tuples, file };
    // const input = document.createElement('input');
    // input.type = 'hidden';
    // input.name = 'json';
    // input.value = JSON.stringify(data);
    // form.appendChild(input);

    // document.body.appendChild(form);
    // form.submit();
    fetch('/submit-titles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tuples, file })
    })
    .then(res => res.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect; // Navigate manually
        } else {
            alert(data.message);
        }
    });
}


// // function to enter categories
// function enterCategories() {
//     // while (ture) {
//         const categories = prompt("Enter categories as a python list, e.g., ['cat1', 'cat2', ...]:");
//         if (categories) {
//             try {
//                 // Evaluate the input to convert it into an array
//                 const categoriesArray = eval(categories);
//                 if (Array.isArray(categoriesArray)) {
//                     const p = document.createElement('p');
//                     p.innerText = `Categories: ${JSON.stringify(categoriesArray)}`;

//                     // send to server
//                     fetch('/submit-categories', {
//                         method: 'POST',
//                         headers: { 'Content-Type': 'application/json' },
//                         body: JSON.stringify({ categories: categoriesArray, file })
//                     })
//                     .then(res => res.json())
//                     .then(data => {
//                         if (data.redirect) {
//                             window.location.href = data.redirect; // Navigate manually
//                         } else {
//                             alert(data.message);
//                         }
//                     });

//                     formContainer.appendChild(p);

//                     // break; // Exit the loop if input is valid
//                 } else {
//                     alert("Please enter a valid Python list.");
//                 }
//             } catch (e) {
//                 alert("Error parsing categories. Please ensure it's a valid Python list.");
//             }
//         }
//     // }
// }

