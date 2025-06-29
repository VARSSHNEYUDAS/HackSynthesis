// File: server.js
require("dotenv").config();
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const { CloudinaryStorage } = require("multer-storage-cloudinary");
const cloudinary = require("cloudinary").v2;

// Config Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUD_NAME,
  api_key: process.env.CLOUD_API_KEY,
  api_secret: process.env.CLOUD_API_SECRET,
});

const app = express();
app.use(cors());
app.use(express.json());

// Configure multer to use cloudinary
const storage = new CloudinaryStorage({
  cloudinary: cloudinary,
  params: {
    folder: "recycLens",
    allowed_formats: ["jpg", "png", "jpeg"],
  },
});

const upload = multer({ storage });

// Upload endpoint
app.post("/api/upload", upload.single("file"), (req, res) => {
  const imageUrl = req.file.path;
  const { name } = req.body;

  // For demo, simulate product classification logic
  let result = "Unknown";
  if (name.toLowerCase().includes("bottle")) {
    result = "Recyclable";
  } else if (name.toLowerCase().includes("jeans")) {
    result = "Reusable - consider DIY crafts";
  } else if (name.toLowerCase().includes("phone")) {
    result = "Repairable - look for parts";
  }

  res.json({
    message: "Upload successful",
    imageUrl,
    productName: name,
    suggestion: result,
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

const cloudinary = require('cloudinary').v2;
require('dotenv').config();

cloudinary.config({
  cloud_name: process.env.CLOUD_NAME,
  api_key: process.env.CLOUD_API_KEY,
  api_secret: process.env.CLOUD_API_SECRET,
});

module.exports = cloudinary;

const { CloudinaryStorage } = require('multer-storage-cloudinary');
const multer = require('multer');

const storage = new CloudinaryStorage({
  cloudinary: cloudinary,
  params: {
    folder: 'recycLens',
    allowed_formats: ['jpg', 'png', 'jpeg'],
    resource_type: 'auto',
  },
});

const upload = multer({ storage });

app.post('/api/upload', upload.single('file'), (req, res) => {
  const imageUrl = req.file.path;
  // handle the rest of your logic
});
