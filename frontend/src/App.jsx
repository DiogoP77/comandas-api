import { BrowserRouter } from "react-router-dom";

import { CssBaseline } from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";

import { useMemo, useState } from "react";

import { getTheme } from "./theme";

import { AuthProvider } from "./context/AuthContext";

import Navbar from "./components/common/Navbar";
import AppRoutes from "./routes/Router";

import SidebarProfile from "./components/common/SidebarProfile";

function App() {
  const [mode, setMode] = useState("light");

  const theme = useMemo(() => getTheme(mode), [mode]);

  const toggleTheme = () => {
    setMode((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <BrowserRouter>
        <AuthProvider>

          {/* NAVBAR GLOBAL */}
          <Navbar mode={mode} toggleTheme={toggleTheme} />

          {/* FOTO FIXA GLOBAL (OBRIGATÓRIO DA ATIVIDADE) */}
          <SidebarProfile />

          {/* ROTAS DA APLICAÇÃO */}
          <AppRoutes />

        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;

//Diogo Pereira