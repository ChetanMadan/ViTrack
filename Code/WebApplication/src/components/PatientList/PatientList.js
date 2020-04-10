import React, { useState } from "react";
import "./PatientList.css";
import { Link } from "react-router-dom";

const PatientList = (props) => {
  return (
    <div className="col-sm-8 col-md-6 col-lg-5 col-xl-4">
      <div className="card m-4">
        <div className="card-body text-center text-dark">
          <h4 className="card-title">Saksham Madan</h4>
          <h6 className="card-subtitle mb-2 text-muted">Patient #1</h6>
          <hr />
          <div className="text-left">
            <h6>Date : {}</h6>
            <h6>Body Temperature : dsds</h6>
            <h6>Pulse Rate : dsds</h6>
          </div>
          <div class="text-right">
            <Link to="/patient-1" className="card-link">
              More Details..
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientList;
