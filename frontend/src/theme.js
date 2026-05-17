import { createTheme } from "@mui/material/styles";

export const getTheme = (mode) =>
  createTheme({

    palette: {
      mode,

      primary: {
        main: "#f59e0b",
      },

      secondary: {
        main: "#38bdf8",
      },

      background: {
        default:
          mode === "dark"
            ? "#0f172a"
            : "#f8fafc",

        paper:
          mode === "dark"
            ? "#1e293b"
            : "#ffffff",
      },

      text: {
        primary:
          mode === "dark"
            ? "#ffffff"
            : "#1e293b",

        secondary:
          mode === "dark"
            ? "#cbd5e1"
            : "#64748b",
      },
    },

    typography: {
      fontFamily:
        '"Inter", "Roboto", sans-serif',
    },

    shape: {
      borderRadius: 12,
    },

    components: {

      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
          },
        },
      },

      MuiCard: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
          },
        },
      },

      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: "none",
            fontWeight: 600,
          },
        },
      },
    },
  });