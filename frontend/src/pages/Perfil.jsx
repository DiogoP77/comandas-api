import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  Grid,
  Divider,
  Chip
} from "@mui/material";

import {
  Person,
  Email,
  Badge,
  Verified
} from "@mui/icons-material";

import PageLayout from "../components/common/PageLayout";

import fotoPerfil from "../assets/minha-foto.jpeg";

function Perfil() {

  return (
    <PageLayout title="Meu Perfil">

      <Grid container spacing={3}>

        {/* CARD PRINCIPAL */}
        <Grid item xs={12} md={4}>

          <Card
            sx={{
              borderRadius: 4,
              textAlign: "center",
              p: 3,
              height: "100%"
            }}
          >

            <Avatar
              src={fotoPerfil}
              sx={{
                width: 170,
                height: 170,
                mx: "auto",
                mb: 2,
                border: "4px solid",
                borderColor: "primary.main"
              }}
            />

            <Typography
              variant="h5"
              sx={{
                fontWeight: 700,
                mb: 1
              }}
            >
              Diogo
            </Typography>

            <Chip
              icon={<Verified />}
              label="Administrador"
              color="primary"
            />

          </Card>

        </Grid>

        {/* INFORMAÇÕES */}
        <Grid item xs={12} md={8}>

          <Card
            sx={{
              borderRadius: 4,
              height: "100%"
            }}
          >

            <CardContent>

              <Typography
                variant="h5"
                sx={{
                  mb: 3,
                  fontWeight: 700
                }}
              >
                Informações do Usuário
              </Typography>

              <Divider sx={{ mb: 3 }} />

              {/* Nome */}
              <Box sx={{ mb: 3 }}>

                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    mb: 1
                  }}
                >
                  <Person color="primary" />

                  <Typography
                    variant="body2"
                    color="text.secondary"
                  >
                    Nome
                  </Typography>
                </Box>

                <Typography
                  variant="body1"
                  sx={{ fontWeight: 600 }}
                >
                  Diogo
                </Typography>

              </Box>

              {/* Email */}
              <Box sx={{ mb: 3 }}>

                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    mb: 1
                  }}
                >
                  <Email color="primary" />

                  <Typography
                    variant="body2"
                    color="text.secondary"
                  >
                    E-mail
                  </Typography>
                </Box>

                <Typography
                  variant="body1"
                  sx={{ fontWeight: 600 }}
                >
                  diogo@email.com
                </Typography>

              </Box>

              {/* Cargo */}
              <Box>

                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    mb: 1
                  }}
                >
                  <Badge color="primary" />

                  <Typography
                    variant="body2"
                    color="text.secondary"
                  >
                    Cargo
                  </Typography>
                </Box>

                <Typography
                  variant="body1"
                  sx={{ fontWeight: 600 }}
                >
                  Administrador do Sistema
                </Typography>

              </Box>

            </CardContent>

          </Card>

        </Grid>

      </Grid>

    </PageLayout>
  );
}

export default Perfil;