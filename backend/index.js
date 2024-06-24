const express = require("express");
const multer = require("multer");
const pdfParse = require("pdf-parse");
const gTTS = require("gtts");
const fs = require("fs");
const path = require("path");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(express.static("uploads"));

app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    const fileBuffer = fs.readFileSync(req.file.path);
    const pdfData = await pdfParse(fileBuffer);
    const text = pdfData.text;

    const gtts = new gTTS(text, "en");
    const audioFilePath = `uploads/${req.file.filename}.mp3`;
    gtts.save(audioFilePath, (err) => {
      if (err) {
        return res.status(500).send("Error converting text to speech");
      }
      res.send({ audioUrl: `/${audioFilePath}` });
    });
  } catch (error) {
    res.status(500).send("Error processing PDF file");
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
