import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
} from "@mui/material";

import {
  People,
  Group,
  RestaurantMenu,
  ReceiptLong,
  AttachMoney,
} from "@mui/icons-material";

import PageLayout from "../components/common/PageLayout";

function Dashboard() {

  const cards = [
    {
      title: "Clientes",
      value: 128,
      icon: <Group sx={{ fontSize: 40 }} />,
      color: "#3b82f6",
    },
    {
      title: "Funcionários",
      value: 12,
      icon: <People sx={{ fontSize: 40 }} />,
      color: "#10b981",
    },
    {
      title: "Produtos",
      value: 45,
      icon: <RestaurantMenu sx={{ fontSize: 40 }} />,
      color: "#f59e0b",
    },
    {
      title: "Comandas Abertas",
      value: 8,
      icon: <ReceiptLong sx={{ fontSize: 40 }} />,
      color: "#ef4444",
    },
    {
      title: "Faturamento",
      value: "R$ 4.590",
      icon: <AttachMoney sx={{ fontSize: 40 }} />,
      color: "#8b5cf6",
    },
  ];

  return (
    <PageLayout title="Dashboard">

      <Grid container spacing={3}>

        {cards.map((card, index) => (

          <Grid
            item
            xs={12}
            sm={6}
            md={4}
            lg={3}
            key={index}
          >

            <Card
              sx={{
                borderRadius: 4,
                transition: "0.3s",
                backgroundColor: "background.paper",
                color: "text.primary",

                "&:hover": {
                  transform: "translateY(-5px)",
                  boxShadow: 6,
                },
              }}
            >

              <CardContent>

                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >

                  <Box>

                    <Typography
                      variant="body2"
                      color="text.secondary"
                    >
                      {card.title}
                    </Typography>

                    <Typography
                      variant="h4"
                      sx={{
                        fontWeight: 700,
                        mt: 1,
                        color: "text.primary",
                      }}
                    >
                      {card.value}
                    </Typography>

                  </Box>

                  <Box
                    sx={{
                      width: 70,
                      height: 70,
                      borderRadius: "50%",
                      backgroundColor: card.color,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      color: "white",
                      boxShadow: 3,
                    }}
                  >
                    {card.icon}
                  </Box>

                </Box>

              </CardContent>

            </Card>

          </Grid>

        ))}

      </Grid>

    </PageLayout>
  );
}

export default Dashboard;