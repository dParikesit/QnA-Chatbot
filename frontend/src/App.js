import "./App.css";
import "bulma/css/bulma.css";

function App() {
  return (
    <div class="is-flex is-flex-direction-row is-justify-content-center">
      <div class="container is-mobile">
        <div class="notification is-primary">
          Halo, saya chatty! Chatbot bahasa Indonesia milik Prosa.Ai. Kamu boleh tanya apa saja berkaitan Prosa.Ai kepada saya
        </div>
        <div class="table-container">
          <table class="table is-fullwidth">
            <tbody>
              <tr>
                <td>Halo 1.1</td>
                <td>Halo 2.1</td>
              </tr>
              <tr>
                <td>Halo 1.1</td>
                <td>Halo 2.1</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="field is-flex">
          <p class="control is-flex-grow-1">
            <input class="input" type="password" placeholder="Password"></input>
          </p>
          <button class="button is-success">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
