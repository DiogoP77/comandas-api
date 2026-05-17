// arquivo de rotas da aplicação usando React Router v6

import { Suspense, lazy } from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import PrivateRoute from "./PrivateRoute";
import RestrictedRoute from "./RestrictedRoute";

// ============================
// Lazy Loading
// ============================

const Dashboard = lazy(() => import("../pages/Dashboard"));

const FuncionarioList = lazy(() => import("../pages/FuncionarioList"));
const FuncionarioForm = lazy(() => import("../pages/FuncionarioForm"));

const ClienteList = lazy(() => import("../pages/ClienteList"));
const ClienteForm = lazy(() => import("../pages/ClienteForm"));

const ProdutoList = lazy(() => import("../pages/ProdutoList"));
const ProdutoForm = lazy(() => import("../pages/ProdutoForm"));

const ComandaList = lazy(() => import("../pages/ComandaList"));

const CaixaList = lazy(() => import("../pages/CaixaList"));

const LoginForm = lazy(() =>
  import("../components/forms/LoginForm")
);

const Perfil = lazy(() => import("../pages/Perfil"));

const NotFound = lazy(() => import("../pages/NotFound"));

// ============================
// Loader
// ============================

const Loading = () => (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      fontSize: "20px",
      fontWeight: "bold",
    }}
  >
    Carregando...
  </div>
);

// ============================
// Rotas
// ============================

const AppRoutes = () => {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>

        {/* Redirecionamento inicial */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* ========================= */}
        {/* Rotas públicas */}
        {/* ========================= */}
        <Route path="/produtos/publica" element={<ProdutoList />} />

        {/* ========================= */}
        {/* Login restrito */}
        {/* ========================= */}
        <Route
          path="/login"
          element={
            <RestrictedRoute>
              <LoginForm />
            </RestrictedRoute>
          }
        />

        {/* ========================= */}
        {/* Rotas protegidas */}
        {/* ========================= */}
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        {/* Produtos */}
        <Route
          path="/produtos"
          element={
            <PrivateRoute>
              <ProdutoList />
            </PrivateRoute>
          }
        />

        <Route
          path="/produto"
          element={
            <PrivateRoute>
              <ProdutoForm />
            </PrivateRoute>
          }
        />

        {/* Funcionários */}
        <Route
          path="/funcionarios"
          element={
            <PrivateRoute>
              <FuncionarioList />
            </PrivateRoute>
          }
        />

        <Route
          path="/funcionario"
          element={
            <PrivateRoute>
              <FuncionarioForm />
            </PrivateRoute>
          }
        />

        {/* Clientes */}
        <Route
          path="/clientes"
          element={
            <PrivateRoute>
              <ClienteList />
            </PrivateRoute>
          }
        />

        <Route
          path="/cliente"
          element={
            <PrivateRoute>
              <ClienteForm />
            </PrivateRoute>
          }
        />

        {/* Comandas */}
        <Route
          path="/comandas"
          element={
            <PrivateRoute>
              <ComandaList />
            </PrivateRoute>
          }
        />

        {/* Caixa */}
        <Route
          path="/caixa"
          element={
            <PrivateRoute>
              <CaixaList />
            </PrivateRoute>
          }
        />

        {/* Perfil */}
        <Route
          path="/perfil"
          element={
            <PrivateRoute>
              <Perfil />
            </PrivateRoute>
          }
        />

        {/* 404 */}
        <Route path="*" element={<NotFound />} />

      </Routes>
    </Suspense>
  );
};

export default AppRoutes;