import React from "react";
import styles from "./header.module.scss";
import { Image } from "@arco-design/web-react";
import logo from "../assets/images/logo.png";

export default function Header() {
  return (
    <div className={styles.header}>
      <div className={styles.systemName}>
        <Image className={styles.logo} width={48} src={logo} alt="logo" />
        <p>Color</p>
        <p style={{ color: "#007c36" }}>Synth</p>
      </div>
    </div>
  );
}
