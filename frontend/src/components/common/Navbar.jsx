import MinhaFoto from "../../assets/minha-foto.jpeg";

import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Tooltip,
  Avatar,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";

import {
  Dashboard,
  People,
  Group,
  RestaurantMenu,
  Receipt,
  PointOfSale,
  Logout,
  AccountCircle,
  Menu as MenuIcon,
  Brightness4,
  Brightness7,
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useState } from "react";

const Navbar = ({ mode, toggleTheme }) => {

  const navigate = useNavigate();

  const {
    isAuthenticated,
    logout,
    user,
  } = useAuth();

  const [mobileDrawerOpen, setMobileDrawerOpen] =
    useState(false);

  const handleLogout = () => {
    logout();
  };

  const handleDrawerToggle = () => {
    setMobileDrawerOpen((prev) => !prev);
  };

  // =========================
  // MENU
  // =========================

  const menuItems = [
    {
      label: "Dashboard",
      icon: <Dashboard />,
      path: "/home",
    },
    {
      label: "Funcionários",
      icon: <People />,
      path: "/funcionarios",
    },
    {
      label: "Clientes",
      icon: <Group />,
      path: "/clientes",
    },
    {
      label: "Produtos",
      icon: <RestaurantMenu />,
      path: "/produtos",
    },
    {
      label: "Comandas",
      icon: <Receipt />,
      path: "/comandas",
    },
    {
      label: "Caixa",
      icon: <PointOfSale />,
      path: "/caixa",
    },
  ];

  // =========================
  // DRAWER MOBILE
  // =========================

  const drawer = (
    <Box
      sx={{
        width: 260,
        height: "100%",
        backgroundColor:
          mode === "dark"
            ? "#0f172a"
            : "#ffffff",

        color:
          mode === "dark"
            ? "white"
            : "#1e293b",
      }}
    >

      {/* HEADER */}
      <Box
        sx={{
          p: 3,
          display: "flex",
          alignItems: "center",
          gap: 1,

          borderBottom:
            mode === "dark"
              ? "1px solid rgba(255,255,255,0.1)"
              : "1px solid rgba(0,0,0,0.08)",
        }}
      >

        <RestaurantMenu
          sx={{
            color: "#f59e0b",
          }}
        />

        <Typography
          variant="h6"
          sx={{
            fontWeight: 700,
          }}
        >
          Comandas do Zé
        </Typography>

      </Box>

      {/* PERFIL */}
      <Box
        sx={{
          p: 2,
          display: "flex",
          alignItems: "center",
          gap: 2,
        }}
      >

        <Avatar
          src={MinhaFoto}
          sx={{
            width: 52,
            height: 52,
            border: "2px solid #f59e0b",
            boxShadow: 2,
          }}
        >
          {user?.nome
            ? user.nome.charAt(0).toUpperCase()
            : <AccountCircle />}
        </Avatar>

        <Box>

          <Typography
            sx={{
              fontWeight: 700,
            }}
          >
            {user?.nome || "Usuário"}
          </Typography>

          <Typography
            variant="body2"
            sx={{
              opacity: 0.7,
              fontSize: "0.8rem",
            }}
          >
            Funcionário autenticado
          </Typography>

        </Box>

      </Box>

      <Divider />

      {/* MENU */}
      <List sx={{ mt: 1 }}>

        {menuItems.map((item) => (

          <ListItemButton
            key={item.path}
            onClick={() => {
              navigate(item.path);
              handleDrawerToggle();
            }}
            sx={{
              mx: 1,
              borderRadius: 2,
              mb: 0.5,

              "&:hover": {
                backgroundColor:
                  mode === "dark"
                    ? "rgba(255,255,255,0.08)"
                    : "rgba(0,0,0,0.05)",
              },
            }}
          >

            <ListItemIcon
              sx={{
                color: "#f59e0b",
                minWidth: 40,
              }}
            >
              {item.icon}
            </ListItemIcon>

            <ListItemText primary={item.label} />

          </ListItemButton>

        ))}

      </List>

      <Divider sx={{ my: 2 }} />

      {/* PERFIL */}
      <ListItemButton
        onClick={() => {
          navigate("/perfil");
          handleDrawerToggle();
        }}
        sx={{
          mx: 1,
          borderRadius: 2,

          "&:hover": {
            backgroundColor:
              mode === "dark"
                ? "rgba(255,255,255,0.08)"
                : "rgba(0,0,0,0.05)",
          },
        }}
      >

        <ListItemIcon
          sx={{
            color: "#38bdf8",
            minWidth: 40,
          }}
        >
          <AccountCircle />
        </ListItemIcon>

        <ListItemText primary="Perfil" />

      </ListItemButton>

      {/* TEMA */}
      <ListItemButton
        onClick={toggleTheme}
        sx={{
          mx: 1,
          borderRadius: 2,

          "&:hover": {
            backgroundColor:
              mode === "dark"
                ? "rgba(255,255,255,0.08)"
                : "rgba(0,0,0,0.05)",
          },
        }}
      >

        <ListItemIcon
          sx={{
            color: "#f59e0b",
            minWidth: 40,
          }}
        >
          {mode === "dark"
            ? <Brightness7 />
            : <Brightness4 />}
        </ListItemIcon>

        <ListItemText
          primary={
            mode === "dark"
              ? "Modo Claro"
              : "Modo Escuro"
          }
        />

      </ListItemButton>

      {/* LOGOUT */}
      <ListItemButton
        onClick={handleLogout}
        sx={{
          mx: 1,
          borderRadius: 2,

          "&:hover": {
            backgroundColor:
              "rgba(239,68,68,0.15)",
          },
        }}
      >

        <ListItemIcon
          sx={{
            color: "#ef4444",
            minWidth: 40,
          }}
        >
          <Logout />
        </ListItemIcon>

        <ListItemText primary="Logout" />

      </ListItemButton>

    </Box>
  );

  return (
    <>

      <AppBar
        position="sticky"
        elevation={3}
        sx={{
          background:
            mode === "dark"
              ? "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
              : "linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)",
        }}
      >

        <Toolbar
          sx={{
            minHeight: 70,
            px: { xs: 1, sm: 2 },
          }}
        >

          {/* LOGO */}
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              flexGrow: 1,
              cursor: "pointer",
            }}
            onClick={() => navigate("/home")}
          >

            <RestaurantMenu
              sx={{
                color: "#fff",
                fontSize: 34,
              }}
            />

            <Typography
              variant="h5"
              sx={{
                fontWeight: 800,
                color: "white",

                display: {
                  xs: "none",
                  sm: "block",
                },
              }}
            >
              Comandas do Zé
            </Typography>

            <Typography
              variant="h6"
              sx={{
                fontWeight: 800,
                color: "white",

                display: {
                  xs: "block",
                  sm: "none",
                },
              }}
            >
              Zé
            </Typography>

          </Box>

          {/* LOGADO */}
          {isAuthenticated && (

            <>

              {/* DESKTOP */}
              <Box
                sx={{
                  display: {
                    xs: "none",
                    md: "flex",
                  },

                  alignItems: "center",
                  gap: 1,
                }}
              >

                {menuItems.map((item) => (

                  <Tooltip
                    key={item.path}
                    title={item.label}
                    arrow
                  >

                    <Button
                      color="inherit"
                      startIcon={item.icon}
                      onClick={() =>
                        navigate(item.path)
                      }
                      sx={{
                        borderRadius: 2,
                        textTransform: "none",
                        fontWeight: 600,

                        "&:hover": {
                          backgroundColor:
                            "rgba(255,255,255,0.1)",
                        },
                      }}
                    >
                      {item.label}
                    </Button>

                  </Tooltip>

                ))}

                {/* TEMA */}
                <Tooltip title="Tema" arrow>

                  <IconButton
                    color="inherit"
                    onClick={toggleTheme}
                  >

                    {mode === "dark"
                      ? <Brightness7 />
                      : <Brightness4 />}

                  </IconButton>

                </Tooltip>

                {/* USUÁRIO */}
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    ml: 1,
                  }}
                >

                  <Tooltip title="Perfil" arrow>

                    <IconButton
                      color="inherit"
                      onClick={() =>
                        navigate("/perfil")
                      }
                    >

                      <Avatar
                        src={MinhaFoto}
                        sx={{
                          width: 38,
                          height: 38,
                          border:
                            "2px solid rgba(255,255,255,0.4)",

                          boxShadow: 2,
                        }}
                      >
                        {user?.nome
                          ? user.nome
                              .charAt(0)
                              .toUpperCase()
                          : <AccountCircle />}
                      </Avatar>

                    </IconButton>

                  </Tooltip>

                  <Box
                    sx={{
                      display: {
                        xs: "none",
                        lg: "block",
                      },

                      lineHeight: 1.1,
                    }}
                  >

                    <Typography
                      sx={{
                        fontSize: "0.9rem",
                        fontWeight: 700,
                        color: "#fff",
                      }}
                    >
                      {user?.nome || "Usuário"}
                    </Typography>

                    <Typography
                      sx={{
                        fontSize: "0.75rem",
                        opacity: 0.8,
                        color: "#fff",
                      }}
                    >
                      Funcionário autenticado
                    </Typography>

                  </Box>

                </Box>

                {/* LOGOUT */}
                <Tooltip title="Logout" arrow>

                  <IconButton
                    color="inherit"
                    onClick={handleLogout}
                  >

                    <Logout />

                  </IconButton>

                </Tooltip>

              </Box>

              {/* MOBILE */}
              <Box
                sx={{
                  display: {
                    xs: "flex",
                    md: "none",
                  },

                  alignItems: "center",
                  gap: 1,
                }}
              >

                {/* PERFIL */}
                <IconButton
                  color="inherit"
                  onClick={() =>
                    navigate("/perfil")
                  }
                >

                  <Avatar
                    src={MinhaFoto}
                    sx={{
                      width: 34,
                      height: 34,
                      border:
                        "2px solid rgba(255,255,255,0.4)",
                    }}
                  >
                    {user?.nome
                      ? user.nome
                          .charAt(0)
                          .toUpperCase()
                      : <AccountCircle />}
                  </Avatar>

                </IconButton>

                {/* TEMA */}
                <IconButton
                  color="inherit"
                  onClick={toggleTheme}
                >

                  {mode === "dark"
                    ? <Brightness7 />
                    : <Brightness4 />}

                </IconButton>

                {/* MENU */}
                <IconButton
                  color="inherit"
                  onClick={handleDrawerToggle}
                >

                  <MenuIcon />

                </IconButton>

              </Box>

            </>

          )}

        </Toolbar>

      </AppBar>

      {/* DRAWER */}
      <Drawer
        anchor="left"
        open={mobileDrawerOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: {
            xs: "block",
            md: "none",
          },

          "& .MuiDrawer-paper": {
            width: 260,
            boxSizing: "border-box",
          },
        }}
      >
        {drawer}
      </Drawer>

    </>
  );
};

export default Navbar;