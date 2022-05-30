import Header from "./components/Header";
import Footer from "./components/Footer";
import {Container} from "react-bootstrap";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import HomeScreen from "./screens/HomeScreen";
import PostScreen from "./screens/PostScreen";

function App() {
    return (
        <BrowserRouter>
            <Header/>
            <main>
                <div className="py-2">
                    <Container>
                        <Routes>
                            <Route path='/' element={<HomeScreen/>}/>
                            <Route path='/posts/:id' element={<PostScreen/>}/>
                        </Routes>
                    </Container>
                </div>
            </main>
            <Footer/>
        </BrowserRouter>
    );
}

export default App;
