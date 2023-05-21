import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export const ListMyCats = () => {
  const navigate = useNavigate();
  // const { store, actions } = useContext(Context);
  const [favorites, setFavorites] = useState([]);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("miTokenJWT");

    if (!token) {
      // Mmmmm... no tengo el token, no debería poder acceder a está página de React
      navigate("/login");
    }

    const getAllCats = () => {

      fetch(process.env.BACKEND_URL + "/api/cats", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          setFavorites(data)
        })
        .catch((error) => console.log("error", error));
    };
    getAllCats()
  }, []);

  return (
    <div className="container text-center mt-5">
      <div className="row mt-4">
        {favorites.map((fav, i) => (
          <div className="col-3" key={i}>
            <img src={fav.image_url} />
            <p className="fw-bold text-success">{fav.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
