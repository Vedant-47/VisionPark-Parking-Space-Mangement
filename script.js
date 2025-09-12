// Vehicle selection
const vehicleButtons = document.querySelectorAll(".vehicle");
let selectedVehicle = null;

vehicleButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    vehicleButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedVehicle = btn.dataset.type;

    filterLocations(selectedVehicle);
  });
});

// Restriction rules
const allowedLocations = {
  bike: ["Basement", "Amphitheatre"],
  scooty: ["Basement", "Slope", "Viklang Parking"],
  car: ["NUV School Ground"]
};


// Location buttons
const locationButtons = document.querySelectorAll(".location-btn");
const videoElement = document.getElementById("parkingVideo");
const videoTitle = document.getElementById("video-title");
const videoSection = document.getElementById("video-section");

locationButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const place = btn.dataset.place;

    videoTitle.textContent = `Live Parking Slot Detection - ${place}`;
    videoElement.src = `/video/${place}`; // stream from Flask
    videoSection.classList.remove("hidden");
  });
});
// Videos for each location
const videoSources = {
  "Basement": "videos/location1.mp4",
  "NUV School Ground": "videos/location2.mp4",
  "Viklang Parking": "videos/viklang.mp4",
  "Amphitheatre": "videos/amphitheatre.mp4",
  "Slope": "videos/slope.mp4"
};

// Enable/disable locations based on vehicle type
function filterLocations(vehicle) {
  locationButtons.forEach(btn => {
    if (allowedLocations[vehicle].includes(btn.dataset.place)) {
      btn.disabled = false;
      btn.classList.remove("disabled");
    } else {
      btn.disabled = true;
      btn.classList.add("disabled");
    }
  });
}


// Load video on location click
locationButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const place = btn.dataset.place;

    videoTitle.textContent = `Live Parking Slot Detection - ${place}`;
    videoElement.src = `/video/${place}`; // 🔥 stream from Flask
    videoElement.type = "video/mp4"; // ensure browser treats it right
    videoSection.classList.remove("hidden");
  });
});
