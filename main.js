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

    const url = `http://51.12.208.57:8080/${receivedData.menu_date}.jpeg`;

    const data = {
      url: url,
      menu: JSON.stringify(receivedData.foods),
      date: receivedData.menu_date,
    };

    try {
      // If this not throws an error, that means we already saved the menu_date so we will not create it, we will update it
      const lastSavedItem = await pb
        .collection("menus")
        .getFirstListItem(`url="${url}"`);

      const record = await pb
        .collection("menus")
        .update(lastSavedItem.id, data);
      res.json({ message: "Menu is updated." });
    } catch (error) {
      const record = await pb.collection("menus").create(data);
      res.json({ message: "Creating the menu." });
    }
  } catch (error) {
    res.json({ message: "Error on /save-food" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
