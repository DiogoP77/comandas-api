import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Button,
  Divider
} from "@mui/material";

import {
  Receipt,
  PointOfSale,
  Visibility,
  AttachMoney,
  CheckCircle,
  AccessTime
} from "@mui/icons-material";

import PageLayout from "../components/common/PageLayout";

function ComandaList() {

  const comandas = [
    {
      id: 1,
      mesa: "Mesa 01",
      cliente: "João",
      status: "Aberta",
      total: 89.90
    },
    {
      id: 2,
      mesa: "Mesa 05",
      cliente: "Maria",
      status: "Fechada",
      total: 120.50
    },
    {
      id: 3,
      mesa: "Mesa 08",
      cliente: "Carlos",
      status: "Aberta",
      total: 45.00
    }
  ];

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL"
    }).format(value);

  return (
    <PageLayout title="Comandas">

      <Grid container spacing={3}>

        {comandas.map((comanda) => (

          <Grid
            item
            xs={12}
            md={6}
            lg={4}
            key={comanda.id}
          >

            <Card
              sx={{
                borderRadius: 4,
                transition: "0.25s",

                "&:hover": {
                  transform: "translateY(-6px)",
                  boxShadow: 6
                }
              }}
            >

              <CardContent>

                {/* HEADER */}
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 2
                  }}
                >

                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 1
                    }}
                  >
                    <Receipt color="primary" />

                    <Typography
                      variant="h6"
                      sx={{ fontWeight: 700 }}
                    >
                      {comanda.mesa}
                    </Typography>
                  </Box>

                  <Chip
                    label={comanda.status}
                    color={
                      comanda.status === "Aberta"
                        ? "warning"
                        : "success"
                    }
                    icon={
                      comanda.status === "Aberta"
                        ? <AccessTime />
                        : <CheckCircle />
                    }
                  />

                </Box>

                <Divider sx={{ mb: 2 }} />

                {/* CLIENTE */}
                <Typography
                  variant="body2"
                  color="text.secondary"
                >
                  Cliente
                </Typography>

                <Typography
                  variant="body1"
                  sx={{
                    fontWeight: 600,
                    mb: 2
                  }}
                >
                  {comanda.cliente}
                </Typography>

                {/* TOTAL */}
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    mb: 3
                  }}
                >

                  <AttachMoney color="success" />

                  <Typography
                    variant="h5"
                    sx={{
                      color: "success.main",
                      fontWeight: 700
                    }}
                  >
                    {formatCurrency(comanda.total)}
                  </Typography>

                </Box>

                {/* BOTÕES */}
                <Box
                  sx={{
                    display: "flex",
                    gap: 1
                  }}
                >

                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<PointOfSale />}
                  >
                    Abrir
                  </Button>

                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<Visibility />}
                  >
                    Ver
                  </Button>

                </Box>

              </CardContent>

            </Card>

          </Grid>

        ))}

      </Grid>

    </PageLayout>
  );
}

export default ComandaList;