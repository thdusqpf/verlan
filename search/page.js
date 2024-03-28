"use client";
import React, { useState, useEffect } from "react";
import SearchArea from "../SearchArea";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button, Row, Col } from "react-bootstrap";

const SearchPage = (props) => {
  const [resultText, setResultText] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/process_word", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ keyword: props.searchParams.keyword }),
        });

        if (response.ok) {
          const result = await response.json();
          console.log("백엔드에서 받은 결과:", result);
          setResultText(result);
        } else {
          console.error("Error occurred while processing the word");
        }
      } catch (error) {
        console.error("에러 발생:", error);
      }
    };

    if (props.searchParams.keyword) {
      fetchData();
    }
  }, [props.searchParams.keyword]);

  return (
    <div style={{ border: "1px solid black" }}>
      <h1 style={{ marginTop: "100px", textAlign: "center" }}>Search Result</h1>
      <Row>
        <Col style={{ padding: "20", textAlign: "center" }}>
          <h2 style={{ marginTop: "60px" }}>Definition</h2>
          <Button variant="dark" className="black-btn">
            add my note
          </Button>
        </Col>
        <Col>
          <div className="search-card">
            <h4>{props.searchParams.keyword}</h4>
            {resultText.alternative_texts && resultText.alternative_texts.map((a, i) => ( <p key={i}>Original: {a}</p> ))} 
          </div> 
        </Col> 
      </Row> 
      <div className="search-box"> 
        <h1>Find Another Word</h1> <SearchArea /> 
      </div> 
    </div> 
  ); 
}; 
            
export default SearchPage;