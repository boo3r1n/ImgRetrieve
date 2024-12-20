import React from "react";
import styles from "./index.module.scss";
import Header from "./components/header";
import PromptCard from "./components/promptCard";
import "@arco-design/web-react/dist/css/arco.css";
import santa from "./assets/images/santa.png";
import { Image } from "@arco-design/web-react";
import { useState, useEffect } from "react";
import ResultCard from "./components/resultCard";

function App() {
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  const [prompt, setPrompt] = useState("");

  const handlePromptChange = (inputText) => {
    console.log("Prompt changed:", inputText);
    setPrompt(inputText);
  };
  useEffect(() => {
    const handleResize = () => {
      setScreenWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);
  return (
    <div className={styles.home}>
      <Header />
      <div className={styles.bodyContainer}>
        <div className={styles.bgContainerLeft}>
          <p>ColorSynth</p>
        </div>
        <div className={styles.mainContainer}>
          <PromptCard prompt={prompt} onPromptChange={handlePromptChange} />
          <ResultCard prompt={prompt} />
        </div>

        <div className={styles.bgContainerRight}>
          <p>ColorSynth</p>
          {/* <Image className={styles.santa} width={screenWidth/6} src={santa} alt /> */}
        </div>
      </div>
    </div>
  );
}

export default App;
