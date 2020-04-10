import React, { useState, useEffect } from "react";
import Chart from "../Chart/Chart";
import Footer from "../Footer/Footer";

const Patient = (props) => {
  let title = props.title && props.title.$t;
  let content = props.content && props.content.$t;
  let data = content && content.split(",");
  let bodyTemp = data && data[0];
  bodyTemp = bodyTemp && bodyTemp.replace(/[^\d.-]/g, "");
  let pulse = data && data[1];
  pulse = pulse && pulse.replace(/[^\d.-]/g, "");
  let lat = data && data[2];
  lat = lat && lat.replace(/[^\d.-]/g, "");
  let long = data && data[3];
  long = long && long.replace(/[^\d.-]/g, "");

  return (
    <div>
      <h1 className="text-dark text-center font-weight-bold pt-5">
        Patient No.1
      </h1>
      <h2 className="text-dark text-center font-weight-bold">
        Name : Saksham Madan
      </h2>
      <section className="m-0 mt-5">
        <h4 className="text-dark text-muted text-center mb-4">Details</h4>
        <table
          className="table table-bordered table-hover w-75 mx-auto"
          style={{ borderRadius: "10px" }}
        >
          <thead>
            <tr>
              <th>#</th>
              <th>Date</th>
              <th>Body Temperature</th>
              <th>Pulse Rate</th>
              <th>Latitude</th>
              <th>Longitude</th>
            </tr>
          </thead>
          <tbody id="table_body">
            <tr>
              <td></td>
              <td>{title}</td>
              <td>{bodyTemp}</td>
              <td>{pulse}</td>
              <td>{lat}</td>
              <td>{long}</td>
            </tr>
          </tbody>
        </table>
      </section>
      <section className="m-0 mt-5 d-flex flex-column justify-content-center">
        <h4 className="text-dark text-muted text-center mb-4">
          Current Location
        </h4>

        <div className="mx-auto">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d90738.88252324943!2d77.1587!3d28.713!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390cfd5b347eb62d%3A0x52c2b7494e204dce!2sNew%20Delhi%2C%20Delhi!5e0!3m2!1sen!2sin!4v1586531961883!5m2!1sen!2sin"
            width={600}
            height={450}
            frameborder="5"
            style={{ border: "0" }}
            aria-hidden="false"
            tabindex="0"
          ></iframe>
        </div>
      </section>
      <section className="m-0 mt-5">
        <h4 className="text-dark text-muted text-center mb-4">ECG Graph</h4>
        <Chart />
      </section>
      <Footer />
    </div>
  );
};

export default Patient;
