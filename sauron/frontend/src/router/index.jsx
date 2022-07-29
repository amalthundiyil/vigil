import { Routes, Route } from "react-router-dom";
import { Suspense, useState, useEffect } from "react";
import React from "react";
import Error from "../pages/Error";
import Home from "../pages/Home";
import Header from "../components/Header";
import Dashboard from "../pages/Dashboard";
import axios from "../utils/axios";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";

const Router = () => {
  const [allPackages, setAllPackages] = useState([]);

  const particlesInit = async (main) => {
    console.log(main);

    await loadFull(main);
  };

  const particlesLoaded = (container) => {
    console.log(container);
  };

  useEffect(() => {
    const fetchData = async () => {
      const data = await axios.get("/api/home");
    };
    fetchData().catch(console.error);
  }, []);

  return (
    <Suspense fallback={null}>
      <Header />
      <Particles
        id="tsparticles"
        init={particlesInit}
        loaded={particlesLoaded}
        options={{
          background: {
            color: {
              value: "#eeeee4",
            },
          },
          fpsLimit: 120,
          interactivity: {
            events: {
              onClick: {
                enable: true,
                mode: "push",
              },
              onHover: {
                enable: true,
                mode: "repulse",
              },
              resize: true,
            },
            modes: {
              push: {
                quantity: 4,
              },
              repulse: {
                distance: 200,
                duration: 0.4,
              },
            },
          },
          particles: {
            color: {
              value: "#C0C0C0",
            },
            links: {
              color: "#ffffff",
              distance: 150,
              enable: true,
              opacity: 0.5,
              width: 1,
            },
            collisions: {
              enable: true,
            },
            move: {
              direction: "none",
              enable: true,
              outModes: {
                default: "bounce",
              },
              random: false,
              speed: 2,
              straight: false,
            },
            number: {
              density: {
                enable: true,
                area: 800,
              },
              value: 80,
            },
            opacity: {
              value: 0.5,
            },
            shape: {
              type: "circle",
            },
            size: {
              value: { min: 1, max: 5 },
            },
          },
          detectRetina: true,
        }}
      />
      <Routes>
        <Route path="/" element={<Home data={allPackages} />} />
        <Route path="/home" element={<Home data={allPackages} />} />
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        <Route path="*" element={<Error />} />
      </Routes>
    </Suspense>
  );
};

export default Router;
