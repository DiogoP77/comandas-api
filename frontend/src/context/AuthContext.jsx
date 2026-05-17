import { createContext, useState, useContext } from "react";

// Criação do contexto
const AuthContext = createContext();

// Provider
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return sessionStorage.getItem("loginRealizado") === "true";
  });

  // Login
  const login = (cpf, senha) => {
    if (cpf === "abc" && senha === "bolinhas") {
      setIsAuthenticated(true);
      sessionStorage.setItem("loginRealizado", "true");

      return true;
    }

    return false;
  };

  // Logout
  const logout = () => {
    setIsAuthenticated(false);
    sessionStorage.removeItem("loginRealizado");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook
export const useAuth = () => useContext(AuthContext);