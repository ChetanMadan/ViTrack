import React from "react";
import "./Home.css";
import PatientList from "../PatientList/PatientList";
import { Link } from "react-router-dom";
import Footer from "../Footer/Footer";

const Home = (props) => {
  const title = props.title && props.title.$t;
  const content = props.content && props.content.$t;
  const data = content && content.split(",");
  let bodyTemp = data && data[0];
  bodyTemp = bodyTemp && bodyTemp.replace(/\D/g, "");
  let pulse = data && data[1];
  pulse = pulse && pulse.replace(/\D/g, "");

  console.log(data);
  return (
    <div className="con">
      <nav className="navbar-expand-md navbar-light d-flex align-items-center justify-content-between shadow">
        <div>
          <h3 className="ml-3 text-dark text-monospace font-weight-bold">
            Vi.Track
          </h3>
        </div>
        <div className="d-flex mr-4 ">
          <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
            <ul className="d-sm-flex horizontal-list">
              <li>
                <a href="#"> Home </a>
              </li>
              <li>
                <a href="#about"> About </a>
              </li>
              <li>
                <a href="#patients"> Patients</a>
              </li>

              <li>
                <a href="#contact"> Contact Us </a>
              </li>
            </ul>
          </div>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarNavAltMarkup"
            aria-controls="navbarNavAltMarkup"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
        </div>
      </nav>

      <div>
        <section id="about">
          <h2 className="text-dark text-center">About</h2>

          <div id="para">
            <p className="text-dark">
              The application provides a way for people whose relatives are
              affected by the pandemic to check and monitor the health and
              status of the infected patient. This would be extremely helpful
              for people as confirmed COVID 19 patients are kept in complete
              isolation and are not allowed to have visitors throughout their
              course of treatment. The setup consists of a hardware module
              equipped with sensors that read the vital signs of the patient and
              send the data to an online server. The data can be viewed and
              accessed through this web application by family members of the
              patient, in real-time. To avoid breaching in the privacy of the
              patients, the user data is deleted after regular time intervals.
              This web application utilizes a machine learning algorithm
              (XGBoost) to read the data and detect any anomalies to notify the
              appropriate parties in case the patient's health starts to
              deteriorate abruptly.
            </p>
          </div>
        </section>

        <section id="patients">
          <h2 className="text-dark text-center">Patients</h2>
          {/* <PatientList date={state} /> */}
          <div className="col-sm-8 col-md-6 col-lg-5 col-xl-4">
            <div className="card m-4">
              <div className="card-body text-center text-dark">
                <h4 className="card-title">Saksham Madan</h4>
                <h6 className="card-subtitle mb-2 text-muted">Patient #1</h6>
                <hr />
                <div className="text-left">
                  <h6>Date : {title}</h6>
                  <h6>Body Temperature : {bodyTemp}</h6>
                  <h6>Pulse Rate : {pulse}</h6>
                </div>
                <div className="text-right">
                  <Link to="/patient-1" className="card-link">
                    More Details..
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
        <Footer />
      </div>
    </div>
  );
};

export default Home;
