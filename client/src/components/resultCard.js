import React from "react";
import styles from "./result.module.scss";
import { Button, Input } from "@arco-design/web-react";
import axios from "axios";
import { Image } from "@arco-design/web-react";
import { useState, useEffect } from "react";
import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-webgl";
import * as echarts from "echarts";

export default function ResultCard({ prompt }) {
  const [imgResult, setImgResult] = useState("");
  const [topColors, setTopColors] = useState([]);
  const [reasons, setReasons] = useState(
    "Decorated tree, presents, red and gold ornaments, fireplace, snowflakes, garlands, candlelight"
  );

  useEffect(() => {
    console.log("Prompt changed!!!!", prompt);
    axios
      .post("http://127.0.0.1:5050/text-to-image", { text: prompt })
      .then((response) => {
        const { image_url, top_colors } = response.data;
        setImgResult(image_url);
        setTopColors(top_colors);
        console.log("Top colors:", top_colors);
      })
      .catch((error) => {
        console.error("Error fetching image:", error);
      });
  }, [prompt]);

  useEffect(() => {
    const colorData = topColors.map((color, index) => ({
      value: index + 1,
      name: `Color ${index + 1}`,
      itemStyle: { color },
    }));

    const pieChart = echarts.init(document.getElementById("pie"));
    pieChart.setOption({
      series: [
        {
          type: "pie",
          data: colorData,
          label: {
            show: false,
          },
        },
      ],
      legend: {
        show: false,
      },
    });

    const lineChart = echarts.init(document.getElementById("line"));

    const categories = ["TY", "SS", "QG", "SY", "DD"];

    lineChart.setOption({
      legend: {
        data: categories,
        show: false,
      },
      xAxis: {
        show: false,
      },
      yAxis: {
        show: false,
      },
      singleAxis: {
        show: false,
        //   xAxis: { show: false },

        type: "time",
        axisTick: { show: false },
        axisLabel: { show: false },
        axisLine: { show: false },
        splitLine: {
          show: false,
        },
        itemStyle: { color: "white" },
      },
      series: [
        {
          type: "themeRiver",
          label: {
            show: false,
          },
          data: [
            ["2015/11/08", 35, "TY"],
            ["2015/11/09", 36, "TY"],
            ["2015/11/10", 37, "TY"],
            ["2015/11/11", 22, "TY"],
            ["2015/11/12", 24, "TY"],
            ["2015/11/13", 26, "TY"],
            ["2015/11/14", 34, "TY"],
            ["2015/11/15", 21, "TY"],
            ["2015/11/16", 18, "TY"],
            ["2015/11/17", 45, "TY"],
            ["2015/11/18", 32, "TY"],
            ["2015/11/19", 35, "TY"],
            ["2015/11/20", 30, "TY"],
            ["2015/11/21", 28, "TY"],
            ["2015/11/22", 27, "TY"],
            ["2015/11/23", 26, "TY"],
            ["2015/11/24", 15, "TY"],
            ["2015/11/25", 30, "TY"],
            ["2015/11/26", 35, "TY"],
            ["2015/11/27", 42, "TY"],
            ["2015/11/28", 42, "TY"],
            ["2015/11/08", 21, "SS"],
            ["2015/11/09", 25, "SS"],
            ["2015/11/10", 27, "SS"],
            ["2015/11/11", 23, "SS"],
            ["2015/11/12", 24, "SS"],
            ["2015/11/13", 21, "SS"],
            ["2015/11/14", 35, "SS"],
            ["2015/11/15", 39, "SS"],
            ["2015/11/16", 40, "SS"],
            ["2015/11/17", 36, "SS"],
            ["2015/11/18", 33, "SS"],
            ["2015/11/19", 43, "SS"],
            ["2015/11/20", 40, "SS"],
            ["2015/11/21", 34, "SS"],
            ["2015/11/22", 28, "SS"],
            ["2015/11/23", 26, "SS"],
            ["2015/11/24", 37, "SS"],
            ["2015/11/25", 41, "SS"],
            ["2015/11/26", 46, "SS"],
            ["2015/11/27", 47, "SS"],
            ["2015/11/28", 41, "SS"],
            ["2015/11/08", 10, "QG"],
            ["2015/11/09", 15, "QG"],
            ["2015/11/10", 35, "QG"],
            ["2015/11/11", 38, "QG"],
            ["2015/11/12", 22, "QG"],
            ["2015/11/13", 16, "QG"],
            ["2015/11/14", 7, "QG"],
            ["2015/11/15", 2, "QG"],
            ["2015/11/16", 17, "QG"],
            ["2015/11/17", 33, "QG"],
            ["2015/11/18", 40, "QG"],
            ["2015/11/19", 32, "QG"],
            ["2015/11/20", 26, "QG"],
            ["2015/11/21", 35, "QG"],
            ["2015/11/22", 40, "QG"],
            ["2015/11/23", 32, "QG"],
            ["2015/11/24", 26, "QG"],
            ["2015/11/25", 22, "QG"],
            ["2015/11/26", 16, "QG"],
            ["2015/11/27", 22, "QG"],
            ["2015/11/28", 10, "QG"],
            ["2015/11/08", 10, "SY"],
            ["2015/11/09", 15, "SY"],
            ["2015/11/10", 35, "SY"],
            ["2015/11/11", 38, "SY"],
            ["2015/11/12", 22, "SY"],
            ["2015/11/13", 16, "SY"],
            ["2015/11/14", 7, "SY"],
            ["2015/11/15", 2, "SY"],
            ["2015/11/16", 17, "SY"],
            ["2015/11/17", 33, "SY"],
            ["2015/11/18", 40, "SY"],
            ["2015/11/19", 32, "SY"],
            ["2015/11/20", 26, "SY"],
            ["2015/11/21", 35, "SY"],
            ["2015/11/22", 4, "SY"],
            ["2015/11/23", 32, "SY"],
            ["2015/11/24", 26, "SY"],
            ["2015/11/25", 22, "SY"],
            ["2015/11/26", 16, "SY"],
            ["2015/11/27", 22, "SY"],
            ["2015/11/28", 10, "SY"],
            ["2015/11/08", 10, "DD"],
            ["2015/11/09", 15, "DD"],
            ["2015/11/10", 35, "DD"],
            ["2015/11/11", 38, "DD"],
            ["2015/11/12", 22, "DD"],
            ["2015/11/13", 16, "DD"],
            ["2015/11/14", 7, "DD"],
            ["2015/11/15", 2, "DD"],
            ["2015/11/16", 17, "DD"],
            ["2015/11/17", 33, "DD"],
            ["2015/11/18", 4, "DD"],
            ["2015/11/19", 32, "DD"],
            ["2015/11/20", 26, "DD"],
            ["2015/11/21", 35, "DD"],
            ["2015/11/22", 40, "DD"],
            ["2015/11/23", 32, "DD"],
            ["2015/11/24", 26, "DD"],
            ["2015/11/25", 22, "DD"],
            ["2015/11/26", 16, "DD"],
            ["2015/11/27", 22, "DD"],
            ["2015/11/28", 10, "DD"],
          ],
          itemStyle: {
            color: (params) => {
              const categoryIndex = categories.indexOf(params.value[2]);
              return topColors[categoryIndex % topColors.length]; // 取颜色
            },
          },
        },
      ],
    });

    const barChart = echarts.init(document.getElementById("bar"));
    barChart.setOption({
      grid: {
        show: false,
        left: 30,
        right: 30,
        top: 30,
        bottom: 30,
        containLabel: false,
      },
      xAxis: {
        type: "category",
        show: false,
        data: topColors.map((_, index) => `Color ${index + 1}`), // 数据仍需保留
      },
      yAxis: {
        type: "value",
        show: false,
      },
      series: [
        {
          type: "bar",
          data: colorData,
          label: {
            show: false,
          },
        },
      ],
    });
  }, [topColors]);

  return (
    <div className={styles.card}>
      <div className={styles.head}>
        <div className={styles.title}>Result</div>
      </div>
      <div className={styles.imgWithColors}>
        <div className={styles.imageContainer}>
          {imgResult ? (
            <img
              className={styles.retrievedImage}
              src={imgResult}
              alt="Result"
            />
          ) : (
            <p>Loading...</p>
          )}
        </div>
        <div className={styles.colorsContainer}>
          <div className={styles.palette}>
            <div className={styles.title}>Color Palette</div>
            {/* <Button type="text" className={styles.button}>
              Copy
            </Button> */}
          </div>
          <div className={styles.colorItems}>
            {topColors ? (
              topColors.map((color, index) => (
                <div
                  key={index}
                  style={{
                    backgroundColor: color,
                    width: "20%",
                    height: "100%",
                  }}
                ></div>
              ))
            ) : (
              <p>Loading...</p>
            )}
          </div>
          <div className={styles.palette}>
            <div className={styles.title}>Reasons</div>
          </div>
          <div className={styles.reasonContainer}>{reasons}</div>
        </div>
      </div>
      <div className={styles.chartContainer}>
        <div className={styles.chartTitle}>Recommendation</div>
        <div className={styles.chartItems}>
          <div className={styles.chartItem} id="pie"></div>
          <div className={styles.chartItem} id="bar"></div>
          <div className={styles.chartItem} id="line"></div>
        </div>
      </div>
    </div>
  );
}
