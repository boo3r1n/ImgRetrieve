import React from "react";
import styles from "./prompt.module.scss";
import { Button, Input } from "@arco-design/web-react";
import { useState } from "react";
import axios from "axios";
import { IconSend } from "@arco-design/web-react/icon";

export default function PromptCard({ prompt, onPromptChange }) {
  const [inputText, setInputText] = useState("");
  const handleInputChange = (value) => {
    setInputText(value);
  };

  const handleGenerateClick = () => {
    onPromptChange(inputText);
  };
  return (
    <div className={styles.card}>
      <div className={styles.head}>
        <div className={styles.title}>Prompt</div>
        <Button
          type="text"
          className={styles.button}
          onClick={handleGenerateClick}
        >
          Generate
        </Button>
      </div>
      <div className={styles.genPrompt}>
        <Input
          className={styles.input}
          allowClear
          placeholder="Example: A cat"
          onChange={handleInputChange}
        />
  
      </div>
    </div>
  );
}
