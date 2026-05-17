import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button
} from "@mui/material";

import {
  AttachMoney,
  TrendingUp,
  TrendingDown,
  PointOfSale
} from "@mui/icons-material";

import PageLayout from "../components/common/PageLayout";

function CaixaList() {

  const movimentacoes = [
    {
      id: 1,
      descricao: "Venda Comanda #001",
      tipo: "entrada",
      valor: 120.50
    },
    {
      id: 2,
      descricao: "Compra de bebidas",
      tipo: "saida",
      valor: 80.00
    },
    {
      id: 3,
      descricao: "Venda Comanda #002",
      tipo: "entrada",
      valor: 250.90
    }
  ];

  const totalEntradas = movimentacoes
    .filter((m) => m.tipo === "entrada")
    .reduce((acc, item) => acc + item.valor, 0);

  const totalSaidas = movimentacoes
    .filter((m) => m.tipo === "saida")
    .reduce((acc, item) => acc + item.valor, 0);

  const saldo = totalEntradas - totalSaidas;

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL"
    }).format(value);

  return (
    <PageLayout title="Caixa">

      {/* Cards resumo */}
      <Grid container spacing={2} sx={{ mb: 3 }}>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>

              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}
              >
                <Box>
                  <Typography color="text.secondary">
                    Entradas
                  </Typography>

                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 700,
                      color: "success.main"
                    }}
                  >
                    {formatCurrency(totalEntradas)}
                  </Typography>
                </Box>

                <TrendingUp
                  sx={{
                    fontSize: 45,
                    color: "success.main"
                  }}
                />

              </Box>

            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>

              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}
              >
                <Box>
                  <Typography color="text.secondary">
                    Saídas
                  </Typography>

                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 700,
                      color: "error.main"
                    }}
                  >
                    {formatCurrency(totalSaidas)}
                  </Typography>
                </Box>

                <TrendingDown
                  sx={{
                    fontSize: 45,
                    color: "error.main"
                  }}
                />

              </Box>

            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>

              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center"
                }}
              >
                <Box>
                  <Typography color="text.secondary">
                    Saldo
                  </Typography>

                  <Typography
                    variant="h5"
                    sx={{
                      fontWeight: 700,
                      color: "primary.main"
                    }}
                  >
                    {formatCurrency(saldo)}
                  </Typography>
                </Box>

                <AttachMoney
                  sx={{
                    fontSize: 45,
                    color: "primary.main"
                  }}
                />

              </Box>

            </CardContent>
          </Card>
        </Grid>

      </Grid>

      {/* Tabela */}
      <TableContainer component={Paper}>

        <Table>

          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Descrição</TableCell>
              <TableCell>Tipo</TableCell>
              <TableCell>Valor</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>

            {movimentacoes.map((item) => (

              <TableRow key={item.id} hover>

                <TableCell>{item.id}</TableCell>

                <TableCell>
                  {item.descricao}
                </TableCell>

                <TableCell>

                  <Chip
                    label={
                      item.tipo === "entrada"
                        ? "Entrada"
                        : "Saída"
                    }
                    color={
                      item.tipo === "entrada"
                        ? "success"
                        : "error"
                    }
                  />

                </TableCell>

                <TableCell
                  sx={{
                    fontWeight: 600,
                    color:
                      item.tipo === "entrada"
                        ? "success.main"
                        : "error.main"
                  }}
                >
                  {formatCurrency(item.valor)}
                </TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>

      </TableContainer>

    </PageLayout>
  );
}

export default CaixaList;