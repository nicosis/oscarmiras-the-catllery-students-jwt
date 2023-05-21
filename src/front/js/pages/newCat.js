import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export const NewCat = () => {
  const [name, setName] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [alertVariant, setAlertVariant] = useState("");
  const [alertMessage, setAlertMessage] = useState("");

  const navigate = useNavigate();

  const token = localStorage.getItem("miTokenJWT");

  if (!token) {
    // Mmmmm... no tengo el token, no debería poder acceder a está página de React
    navigate('/login');
  }


  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ejercicio 4

    const response = await fetch(process.env.BACKEND_URL + "/api/cat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name, imageUrl }),
    });

    const data = await response.json();

    if (response.ok) {
      setAlertVariant("success");
      setAlertMessage("Gato añadido correctamente");
      setName("");
      setImageUrl("");
    } else {
      setAlertVariant("danger");
      setAlertMessage(data.error || "Error al añadir el gato. Mira la consola o en el terminal del servidor de Python");
    }
  };

  return (
    <div>
      <div className="container">
        <h2 className="text-center mt-4 mb-5">Añadir nuevo Gato</h2>
      </div>
      {alertMessage && (
        <div className={`alert alert-${alertVariant}`} role="alert">
          {alertMessage}
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">
            Nombre del gato
          </label>
          <input
            type="text"
            className="form-control"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="imageUrl" className="form-label">
            URL de la imagen
          </label>
          <input
            type="text"
            className="form-control"
            id="imageUrl"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Añadir Gato
        </button>
      </form>
    </div>
  );
};
