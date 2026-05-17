import { Box, Avatar, Typography } from "@mui/material";
import MinhaFoto from "../../assets/minha-foto.jpeg";

const SidebarProfile = () => {
  return (
    <Box
      sx={{
        position: "fixed",
        left: 10,
        top: "50%",
        transform: "translateY(-50%)",
        width: 80,
        height: 120,
        backgroundColor: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(8px)",
        borderRadius: 3,
        display: { xs: "none", md: "flex" },
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 1,
        zIndex: 999,
        boxShadow: 3,
      }}
    >
      <Avatar
        src={MinhaFoto}
        alt="Meu Perfil"
        sx={{
          width: 50,
          height: 50,
          border: "2px solid #f59e0b",
        }}
      />

      <Typography
        sx={{
          fontSize: 12,
          color: "white",
          fontWeight: 600,
        }}
      >
        Você
      </Typography>
    </Box>
  );
};

export default SidebarProfile;