import "./App.css";
import "bulma/css/bulma.css";
import { w3cwebsocket as W3CWebSocket } from "websocket";
import { useState, useEffect } from "react";

function App() {
  const backend = "";
  const [message, setMessage] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        let id = await fetch(backend + "/id", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        id = await id.json();
        const client = await new W3CWebSocket(
          `ws://localhost:5000/ws/${id}:5000`
        );
        console.log({ client });

        client.onopen = () => {
          console.log(`Websocket connected, id = ${id}`);
        };

        client.onmessage = (newMessage) => {
          setMessage([...message, ["", newMessage.data]]);
        };
      } catch (error) {
        console.log(error);
      }
    })();
  }, []);
  return (
    <div className="is-flex is-flex-direction-row is-justify-content-center">
      <div className="container is-mobile">
        <div className="notification is-primary">
          Halo, saya chatty! Chatbot bahasa Indonesia milik Prosa.Ai. Kamu boleh
          tanya apa saja berkaitan Prosa.Ai kepada saya
        </div>
        <div className="table-container">
          <table className="table is-fullwidth">
            <tbody>
              {message.map((post)=>{
                return(
                  <tr>
                    <td>{post[0]}</td>
                    <td>{post[1]}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        <div className="field is-flex">
          <p className="control is-flex-grow-1">
            <input
              className="input"
              type="password"
              placeholder="Password"
            ></input>
          </p>
          <button className="button is-success">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
