import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Report from './pages/Report';
import AddConcentrate from './pages/AddConcentrate';
import { Toaster } from 'sonner';

export default function App() {
  return (
    <Router>
      <Toaster position="top-right" richColors />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Home />} />
        <Route path="/add" element={<AddConcentrate />} />
        <Route path="/report" element={<Report />} />
      </Routes>
    </Router>
  );
}