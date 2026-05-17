import { useForm, Controller } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useRef, useEffect } from "react";

import { useAuth } from "../../context/AuthContext";
import useValidationRules from "../../hooks/useValidationRules";

import {
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  Avatar
} from "@mui/material";

import {
  RestaurantMenu as MenuIcon
} from "@mui/icons-material";

const LoginForm = () => {

  const validationRules = useValidationRules();

  const navigate = useNavigate();

  const cpfRef = useRef(null);

  useEffect(() => {
    cpfRef.current?.focus();
  }, []);

  const {
    control,
    handleSubmit,
    formState: { errors }
  } = useForm();

  const { login } = useAuth();

  // Submit
  const onSubmit = (data) => {

    const { cpf, senha } = data;

    const success = login(cpf, senha);

    if (success) {
      navigate("/home");
    } else {
      alert("Usuário ou senha inválidos!");
    }
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background:
          "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        p: 2
      }}
    >
      <Paper
        elevation={8}
        sx={{
          p: 4,
          maxWidth: 400,
          width: "100%",
          borderRadius: 3,
          background: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(10px)"
        }}
      >
        <Box sx={{ textAlign: "center", mb: 4 }}>

          <Avatar
            sx={{
              width: 64,
              height: 64,
              bgcolor: "#f59e0b",
              mx: "auto",
              mb: 2
            }}
          >
            <MenuIcon sx={{ fontSize: 32 }} />
          </Avatar>

          <Typography
            variant="h4"
            component="h1"
            sx={{
              fontWeight: 700,
              background:
                "linear-gradient(135deg, #1e293b 0%, #334155 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
              mb: 1
            }}
          >
            Comandas do Zé
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Faça login para acessar o sistema
          </Typography>

        </Box>

        {/* Formulário */}
        <Box
          component="form"
          onSubmit={handleSubmit(onSubmit)}
        >

          {/* Usuário */}
          <Controller
            name="cpf"
            control={control}
            defaultValue=""
            rules={validationRules.cpf}
            render={({ field }) => (
              <TextField
                {...field}
                inputRef={cpfRef}
                fullWidth
                label="Usuário"
                placeholder="Digite seu usuário"
                margin="normal"
                error={!!errors.cpf}
                helperText={errors.cpf?.message}
                inputProps={{
                  maxLength: 11
                }}
                sx={{
                  mb: 2,

                  "& .MuiOutlinedInput-root": {

                    "& fieldset": {
                      transition: "0.2s"
                    },

                    "&.Mui-focused fieldset": {
                      borderColor: "#f59e0b",
                      borderWidth: 2
                    }
                  }
                }}
              />
            )}
          />

          {/* Senha */}
          <Controller
            name="senha"
            control={control}
            defaultValue=""
            rules={validationRules.senha}
            render={({ field }) => (
              <TextField
                {...field}
                fullWidth
                label="Senha"
                type="password"
                placeholder="Digite sua senha"
                margin="normal"
                error={!!errors.senha}
                helperText={errors.senha?.message}
                inputProps={{
                  maxLength: 30
                }}
                sx={{
                  mb: 3,

                  "& .MuiOutlinedInput-root": {

                    "& fieldset": {
                      transition: "0.2s"
                    },

                    "&.Mui-focused fieldset": {
                      borderColor: "#f59e0b",
                      borderWidth: 2
                    }
                  }
                }}
              />
            )}
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            size="large"
            sx={{
              py: 1.5,
              fontWeight: 600,

              background:
                "linear-gradient(135deg, #1e293b 0%, #334155 100%)",

              "&:hover": {
                background:
                  "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
              }
            }}
          >
            Entrar
          </Button>

        </Box>
      </Paper>
    </Box>
  );
};

export default LoginForm;