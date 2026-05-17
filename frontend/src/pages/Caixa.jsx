import {
  Grid,
  Card,
  CardContent,
  Typography,
} from "@mui/material";

import {
  AttachMoney,
  TrendingUp,
  ReceiptLong,
} from "@mui/icons-material";

import PageLayout from "../components/common/PageLayout";

function Caixa() {

  const cards = [
    {
      title: "Total do Dia",
      value: "R$ 2.450",
      icon: <AttachMoney sx={{ fontSize: 40 }} />,
      color: "#10b981",
    },
    {
      title: "Comandas Fechadas",
      value: 18,
      icon: <ReceiptLong sx={{ fontSize: 40 }} />,
      color: "#3b82f6",
    },
    {
      title: "Lucro",
      value: "R$ 1.250",
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      color: "#f59e0b",
    },
  ];

  return (
    <PageLayout title="Caixa">

      <Grid container spacing={3}>

        {cards.map((card, index) => (

          <Grid item xs={12} md={4} key={index}>

            <Card
              sx={{
                borderRadius: 4,
                backgroundColor: "background.paper",
              }}
            >

              <CardContent>

                <Typography
                  color="text.secondary"
                >
                  {card.title}
                </Typography>

                <Typography
                  variant="h4"
                  sx={{
                    fontWeight: 700,
                    mt: 1,
                  }}
                >
                  {card.value}
                </Typography>

              </CardContent>

            </Card>

          </Grid>

        ))}

      </Grid>

    </PageLayout>
  );
}

export default Caixa;