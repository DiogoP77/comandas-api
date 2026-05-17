import {
  Box,
  Card,
  CardContent,
  Typography,
  Avatar,
  Grid,
  Chip,
} from "@mui/material";

import {
  Email,
  Badge,
  Phone,
} from "@mui/icons-material";

import MinhaFoto from "../assets/minha-foto.jpeg";

import PageLayout from "../components/common/PageLayout";

function Profile() {

  return (
    <PageLayout title="Meu Perfil">

      <Card
        sx={{
          borderRadius: 4,
          maxWidth: 900,
          mx: "auto",
          p: 2,
        }}
      >

        <CardContent>

          <Grid
            container
            spacing={4}
            alignItems="center"
          >

            {/* FOTO */}
            <Grid item xs={12} md={4}>

              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                }}
              >

                <Avatar
                  src={MinhaFoto}
                  alt="Minha Foto"
                  sx={{
                    width: 220,
                    height: 220,
                    border: "4px solid #f59e0b",
                    boxShadow: 5,
                  }}
                />

              </Box>

            </Grid>

            {/* DADOS */}
            <Grid item xs={12} md={8}>

              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  mb: 1,
                }}
              >
                Diogo
              </Typography>

              <Chip
                label="Administrador"
                color="warning"
                sx={{ mb: 3 }}
              />

              <Box sx={{ mb: 2 }}>

                <Typography
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                  }}
                >
                  <Email />
                  diogo@email.com
                </Typography>

              </Box>

              <Box sx={{ mb: 2 }}>

                <Typography
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                  }}
                >
                  <Phone />
                  (49) 99999-9999
                </Typography>

              </Box>

              <Box>

                <Typography
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                  }}
                >
                  <Badge />
                  Sistema Comandas do Zé
                </Typography>

              </Box>

            </Grid>

          </Grid>

        </CardContent>

      </Card>

    </PageLayout>
  );
}

export default Profile;