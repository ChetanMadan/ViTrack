import React, { useEffect, useState } from "react";
import "./App.css";
import Home from "./components/Home/Home";
import Patient from "./components/Patient/Patient";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import $ from "jquery";
import Popper from "popper.js";
import "bootstrap/dist/js/bootstrap.bundle.min";

const App = () => {
  const [state, setState] = useState({});

  const handleData = async () => {
    const response = await fetch(
      `https://spreadsheets.google.com/feeds/list/1IITEakWWPwqjM7-QX4fT9-W6V6IIz7rPCT6driLwBKM/od6/public/basic?alt=json`
    );
    const data = await response.json();
    const myData = data.feed.entry;
    const required = myData[myData.length - 1];
    setState(required);
  };
  useEffect(() => {
    handleData();
  }, []);
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/">
          <Home {...state} />
        </Route>
        <Route exact path="/patient-1">
          <Patient {...state} />
        </Route>
      </Switch>
    </BrowserRouter>
  );
};

export default App;
