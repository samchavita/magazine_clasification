const express = require('express');
const multer = require('multer');
const path = require('path');
const { spawn } = require('child_process');
const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/public', express.static(path.join(__dirname, 'public')));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Multer setup
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null,file.originalname.replaceAll(' ', '_')),
});
const upload = multer({ storage });

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Upload endpoint
app.post('/upload', upload.single('pdf'), (req, res) => {
    const pdfPath = `/uploads/${req.file.filename}`;
    res.redirect(`/public/viewer.html?file=${pdfPath}`);
});

// Handle tuple data
app.post('/submit-titles', (req, res) => {
    const tuples = req.body.tuples; // Expecting [{ page: 3, title: "Chapter 1" }, ...]
    const file = req.body.file;
    const python = spawn('python3', ['handle_data.py']);

    // send the tupples and the name of the file to the python script
    python.stdin.write(JSON.stringify({ tuples, file }));
    python.stdin.end();

    python.stdout.on('data', (data) => {
        console.log(`Python Output: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`Python script finished with code ${code}`);
        res.json({ message: 'Data sent to Python script.' });
    });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
