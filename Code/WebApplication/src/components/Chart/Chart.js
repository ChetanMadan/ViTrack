import React, { Component, useState } from "react";
import { Bar, Line, Pie } from "react-chartjs-2";

const Chart = (props) => {
  const [state, setState] = useState({
    chartData: {
      labels: [],
      datasets: [
        {
          label: "ECG",
          data: [],
          backgroundColor: ["rgba(255, 99, 132, 0.6)"],
        },
      ],
    },
  });

  return (
    <div className="chart">
      <Line
        data={state.chartData}
        options={{
          title: {
            display: props.displayTitle,
            fontSize: 25,
          },
          legend: {
            display: props.displayLegend,
            position: props.legendPosition,
          },
        }}
      />
    </div>
  );
};

Chart.defaultProps = {
  displayTitle: true,
  displayLegend: true,
  legendPosition: "right",
  location: "City",
};

export default Chart;
