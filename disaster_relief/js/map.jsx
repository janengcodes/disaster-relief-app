import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { loadModules } from 'esri-loader';

const root = createRoot(document.getElementById("viewDiv"));

export default function Map() {
  const [places, setPlaces] = useState([]);
  const [positionData, setPositionData] = useState({ latitude: 0, longitude: 0 });

  useEffect(() => {
    console.log("HI IM IN MAP");
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setPositionData({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        (error) => console.error("Geolocation error:", error)
      );
    } else {
      console.error("Geolocation is not supported by this browser.");
    }
  }, []);

  useEffect(() => {
    if (positionData.latitude && positionData.longitude) {
      initializeMap(positionData);
    }
  }, [positionData]);

  const initializeMap = async ({ latitude, longitude }) => {
   
    const [
        esriConfig,
        Map,
        MapView,
        locator,
        Graphic,
        reactiveUtils,
    ] = await loadModules([
        "esri/config",
        "esri/Map",
        "esri/views/MapView",
        "esri/rest/locator",
        "esri/Graphic",
        "esri/core/reactiveUtils",
    ]);
      esriConfig.apiKey = "AAPTxy8BH1VEsoebNVZXo8HurA6cdLRhE5w3TTgmOuWwrOC1Y36bl5224oc1XOKrlfvikbr0nzAb71JdF4ptEZvDMET7ZgWMK82H9F367uth3WLHi66EP5vq5hbRVDv9UuewV9aufHfsB9mdvfcwj-CqHUjHtWOdsSAUW0P00wOyh70OAGjF7fnujQTp0a511QdPnMkQ6k3koiaTjp_Lc1M--yk-ajUbUOoxcv7nO6gKV8E.AT1_O2L5risA";

      const map = new Map({
        basemap: "arcgis-navigation",
      });

      const view = new MapView({
        map,
        center: [longitude, latitude],
        zoom: 13,
        container: "viewDiv",
      });

      const categories = [
        "Choose a place type...",
        "Hospital",
        "Power Station",
        "Gas station",
        "Convenience Store",
        "Food",
        "Hotel",
        "Grocery",
      ];

      const findPlaces = (category, pt) => {
        if (category === "Choose a place type...") return;
        locator
          .addressToLocations("http://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer", {
            location: pt,
            categories: [category],
            maxLocations: 25,
            outFields: ["Place_addr", "PlaceName"],
          })
          .then((results) => {
            view.popup.close();
            view.graphics.removeAll();
            setPlaces(results);

            results.forEach((result) => {
              view.graphics.add(
                new Graphic({
                  attributes: result.attributes,
                  geometry: result.location,
                  symbol: {
                    type: "simple-marker",
                    color: "#000000",
                    size: "12px",
                    outline: { color: "#ffffff", width: "2px" },
                  },
                  popupTemplate: {
                    title: "{PlaceName}",
                    content: "{Place_addr}",
                  },
                })
              );
            });
          });
      };

      const handleCategoryChange = (event) => {
        findPlaces(event.target.value, view.center);
      };

       // Create and add the dropdown manually
    const dropdown = document.createElement("select");
    dropdown.className = "esri-widget esri-select";
    dropdown.style.width = "175px";
    dropdown.style.fontFamily = "'Avenir Next W00', sans-serif";
    dropdown.style.fontSize = "1em";

    categories.forEach((category) => {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      dropdown.appendChild(option);
    });

    // Add the dropdown to the map's UI
    view.ui.add(dropdown, "top-right");

    // Handle category change
    dropdown.addEventListener("change", handleCategoryChange);

      reactiveUtils.when(
        () => view.stationary,
        () => findPlaces(categories[0], view.center)
      );
  };

  return <div id="viewDiv"></div>;
}

root.render(<Map />);
