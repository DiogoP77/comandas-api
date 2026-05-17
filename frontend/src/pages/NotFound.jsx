import { Box, Typography, Button } from "@mui/material";
import { SentimentDissatisfied } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
        color: "white",
        px: 2,
        overflow: "hidden",
      }}
    >
      {/* ÍCONE ANIMADO */}
      <motion.div
        initial={{ y: -40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        <SentimentDissatisfied
          sx={{ fontSize: 110, color: "#f59e0b", mb: 2 }}
        />
      </motion.div>

      {/* 404 GLITCH */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Typography
          sx={{
            fontSize: { xs: "5rem", md: "7rem" },
            fontWeight: 900,
            position: "relative",
            color: "#f59e0b",

            // glitch simples via sombra
            textShadow:
              "2px 2px #ef4444, -2px -2px #3b82f6",
            animation: "glitch 1s infinite",
          }}
        >
          404
        </Typography>
      </motion.div>

      {/* MENSAGEM */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <Typography variant="h5" sx={{ mt: 2, mb: 1 }}>
          Página perdida no sistema
        </Typography>

        <Typography sx={{ opacity: 0.6, mb: 4 }}>
          Parece que você entrou em uma rota que não existe.
        </Typography>
      </motion.div>

      {/* BOTÕES */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        style={{ display: "flex", gap: 12 }}
      >
        <Button
          variant="outlined"
          onClick={() => navigate(-1)}
          sx={{
            color: "white",
            borderColor: "white",
            px: 3,
            borderRadius: 3,
            "&:hover": {
              borderColor: "#f59e0b",
              color: "#f59e0b",
            },
          }}
        >
          Voltar
        </Button>

        <Button
          variant="contained"
          onClick={() => navigate("/home")}
          sx={{
            backgroundColor: "#f59e0b",
            fontWeight: 700,
            px: 3,
            borderRadius: 3,
            "&:hover": {
              backgroundColor: "#d97706",
            },
          }}
        >
          Dashboard
        </Button>
      </motion.div>

      {/* CSS GLITCH */}
      <style>
        {`
          @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(2px, -2px); }
            60% { transform: translate(-1px, 1px); }
            80% { transform: translate(1px, -1px); }
            100% { transform: translate(0); }
          }
        `}
      </style>
    </Box>
  );
};

export default NotFound;