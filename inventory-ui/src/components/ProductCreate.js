import React, { useState } from "react";
import { Wrapper } from "./Wrapper";
import { useNavigate } from "react-router-dom";

export const ProductCreate = () => {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();

    await fetch(`${process.env.REACT_APP_API_URL}/products`, {
      method: "POST",
      headers: { "content-Type": "application/json" },
      body: JSON.stringify({
        name,
        price,
        quantity,
      }),
    });
    await navigate(-1);
  };

  return (
    <Wrapper>
      <form className="mt-3" onSubmit={submit}>
        <div className="form-floating pb-3">
          <input
            className="form-control"
            placeholder="Name"
            onChange={(e) => setName(e.target.value)}
          />
          <label>Name</label>
        </div>

        <div className="form-floating pb-3">
          <input
            type="number"
            className="form-control"
            placeholder="Price"
            onChange={(e) => setPrice(e.target.value)}
          />
          <label>Price</label>
        </div>

        <div type="number" className="form-floating pb-3">
          <input
            className="form-control"
            placeholder="Quantity"
            onChange={(e) => setQuantity(e.target.value)}
          />
          <label>Quantity</label>
        </div>

        <button className="w-100 btn btn-lg btn-primary" type="submit">
          Submit
        </button>
      </form>
    </Wrapper>
  );
};
