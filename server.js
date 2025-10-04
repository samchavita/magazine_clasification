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
app.use('/extracted', express.static(path.join(__dirname, 'extracted')));
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

    // console.log(`Received tuples: ${JSON.stringify(tuples)}`);

    // send the tupples and the name of the file to the python script
    python.stdin.write(JSON.stringify({ tuples, file }));
    python.stdin.end();

    python.stdout.on('data', (data) => {
        console.log(`Python Output: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`Python script finished with code ${code}`);
        // res.json({ message: 'Data sent to Python script.' });

        const prompt_file_path = "extracted/" + file.split('/').pop() + "/prompt.txt";

        // redirect to download prompt page and send the name of the file
        // res.redirect(`/download_prompt?prompt_file_path=${prompt_file_path}`);

        res.json({ 
          message: 'Data sent to Python script.',
          redirect: `/download_prompt?prompt_file_path=${prompt_file_path}`
        });
    });

});

// Route that renders the HTML with download link
app.get('/download_prompt', (req, res) => {
  const promptFilePath = req.query.prompt_file_path;

  console.log(`in download prompt page: ${promptFilePath}`)

  if (!promptFilePath) {
    return res.status(400).send('Missing prompt_file_path parameter');
  }

  const safeFileName = path.basename(promptFilePath);
  res.sendFile(path.join(__dirname, 'public', 'download_prompt.html'), { filePath: safeFileName });
});

app.get('/download', (req, res) => {
  const file_path = req.query.file_path;
  console.log(`downloading: ${file_path}`);

  if (!file_path) {
    return res.status(400).send('Missing file_path parameter');
  }

  const filePath = file_path; // Assuming the file path is safe and valid

  res.download(filePath, filePath, (err) => {
    if (err) {
      console.error('File download error:', filePath, err);
      res.status(404).send('File not found');
    }
  });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
