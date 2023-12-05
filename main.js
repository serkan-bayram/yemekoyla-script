require("dotenv").config();
const express = require("express");
const PocketBase = require("pocketbase/cjs");
const app = express();
const port = 3000;

app.use(express.json());

app.post("/save-food", async (req, res) => {
  // Process the data received in the POST request
  const receivedData = req.body;
  console.log("Received POST data:", receivedData);

  try {
    const pb = new PocketBase(process.env.dbURL);

    await pb.admins.authWithPassword(
      process.env.dbUsername,
      process.env.dbPassword
    );

    const data = {
      url: `http://51.12.208.57:8080/${receivedData.menu_date}.jpeg`,
      menu: JSON.stringify(receivedData.foods),
      date: receivedData.menu_date,
    };

    const record = await pb.collection("menus").create(data);
  } catch (error) {
    res.json({ message: "Error on /save-food" });
  }

  // Send a response
  res.json({ message: "POST request received and processed." });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
