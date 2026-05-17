import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Snackbar,
  Alert,

  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Card,
  CardContent,
  Typography,
  Box,
  Divider
} from "@mui/material";

import {
  FiberNew
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";
import { useState } from "react";

import PageLayout from "../components/common/PageLayout";
import ActionButtons from "../components/common/ActionButtons";

function ProdutoList() {

  const navigate = useNavigate();

  // =========================
  // STATES
  // =========================

  const [openDialog, setOpenDialog] = useState(false);

  const [produtoSelecionado, setProdutoSelecionado] = useState(null);

  const [openSnackbar, setOpenSnackbar] = useState(false);

  // =========================
  // DADOS MOCKADOS
  // =========================

  const produtos = [
    {
      id: 1,
      nome: "Hambúrguer Clássico",
      descricao: "Pão, carne, alface, tomate e queijo",
      valor_unitario: 25.90,
      foto: "/src/assets/hero.png"
    },
    {
      id: 2,
      nome: "Batata Frita",
      descricao: "Porção média de batata crocante",
      valor_unitario: 12.50,
      foto: "/src/assets/vite.svg"
    },
    {
      id: 3,
      nome: "Refrigerante",
      descricao: "Lata 350ml",
      valor_unitario: 8.00,
      foto: "/src/assets/react.svg"
    }
  ];

  // =========================
  // BOTÃO NOVO
  // =========================

  const actions = (
    <Button
      variant="contained"
      color="primary"
      startIcon={<FiberNew />}
      onClick={() => navigate("/produto")}
      sx={{
        fontWeight: 600,
        px: 2,
        py: 1,
      }}
    >
      Novo
    </Button>
  );

  // =========================
  // FORMATAR MOEDA
  // =========================

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  // =========================
  // AÇÕES
  // =========================

  const handleView = (produto) => {

    alert(
      `Produto: ${produto.nome}\n\nDescrição: ${produto.descricao}\n\nValor: ${formatCurrency(produto.valor_unitario)}`
    );

  };

  const handleEdit = (produto) => {

    navigate(`/produto/${produto.id}`);

  };

  const handleDelete = (produto) => {

    setProdutoSelecionado(produto);

    setOpenDialog(true);

  };

  // =========================
  // CONFIRMAR EXCLUSÃO
  // =========================

  const confirmDelete = () => {

    console.log(
      "Produto excluído:",
      produtoSelecionado
    );

    setOpenDialog(false);

    setOpenSnackbar(true);

  };

  // =========================
  // COLUNAS
  // =========================

  const columns = [
    {
      field: "id",
      headerName: "ID",
    },
    {
      field: "nome",
      headerName: "Nome",
    },
    {
      field: "descricao",
      headerName: "Descrição",
    },
    {
      field: "valor_unitario",
      headerName: "Valor Unitário",
    },
    {
      field: "actions",
      headerName: "Ações",
    },
  ];

  // =========================
  // DESKTOP
  // =========================

  const renderDesktopRow = (produto) => (

    <TableRow key={produto.id} hover>

      <TableCell>
        {produto.id}
      </TableCell>

      <TableCell sx={{ fontWeight: 600 }}>
        {produto.nome}
      </TableCell>

      <TableCell>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            maxWidth: 220,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {produto.descricao}
        </Typography>

      </TableCell>

      <TableCell
        sx={{
          fontWeight: 700,
          color: "success.main",
        }}
      >
        {formatCurrency(produto.valor_unitario)}
      </TableCell>

      <TableCell>

        <ActionButtons
          item={produto}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />

      </TableCell>

    </TableRow>

  );

  // =========================
  // MOBILE
  // =========================

  const renderMobileCard = (produto) => (

    <Card
      key={produto.id}
      sx={{
        mb: 2,
        borderRadius: 3,
      }}
    >

      <CardContent>

        <Box
          sx={{
            display: "flex",
            gap: 2,
            mb: 2,
          }}
        >

          <Box
            sx={{
              width: 70,
              height: 70,
              borderRadius: 2,
              overflow: "hidden",
              backgroundColor: "grey.100",
            }}
          >

            <img
              src={produto.foto}
              alt={produto.nome}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
              }}
            />

          </Box>

          <Box>

            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
              }}
            >
              {produto.nome}
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
            >
              ID: {produto.id}
            </Typography>

          </Box>

        </Box>

        <Divider sx={{ mb: 2 }} />

        <Typography
          variant="body2"
          color="text.secondary"
        >
          Descrição
        </Typography>

        <Typography
          variant="body1"
          sx={{
            mb: 2,
            fontWeight: 500,
          }}
        >
          {produto.descricao}
        </Typography>

        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 2,
          }}
        >

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Valor:
          </Typography>

          <Typography
            variant="body1"
            sx={{
              fontWeight: 700,
              color: "success.main",
            }}
          >
            {formatCurrency(produto.valor_unitario)}
          </Typography>

        </Box>

        <Box
          sx={{
            display: "flex",
            justifyContent: "flex-end",
          }}
        >

          <ActionButtons
            item={produto}
            onView={handleView}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />

        </Box>

      </CardContent>

    </Card>

  );

  // =========================
  // RENDER
  // =========================

  return (

    <PageLayout
      title="Produtos"
      actions={actions}
    >

      {/* DESKTOP */}
      <Box
        sx={{
          display: {
            xs: "none",
            md: "block",
          },
        }}
      >

        <TableContainer component={Paper}>

          <Table>

            <TableHead>

              <TableRow>

                {columns.map((column, index) => (

                  <TableCell
                    key={index}
                    sx={{
                      fontWeight: 700,
                    }}
                  >
                    {column.headerName}
                  </TableCell>

                ))}

              </TableRow>

            </TableHead>

            <TableBody>

              {produtos.map((produto) =>
                renderDesktopRow(produto)
              )}

            </TableBody>

          </Table>

        </TableContainer>

      </Box>

      {/* MOBILE */}
      <Box
        sx={{
          display: {
            xs: "block",
            md: "none",
          },
        }}
      >

        {produtos.map((produto) =>
          renderMobileCard(produto)
        )}

      </Box>

      {/* DIALOG */}
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
      >

        <DialogTitle>
          Confirmar Exclusão
        </DialogTitle>

        <DialogContent>

          <DialogContentText>

            Deseja realmente excluir o produto:

            <strong>
              {" "}
              {produtoSelecionado?.nome}
            </strong>

            ?

          </DialogContentText>

        </DialogContent>

        <DialogActions>

          <Button
            onClick={() => setOpenDialog(false)}
          >
            Cancelar
          </Button>

          <Button
            color="error"
            variant="contained"
            onClick={confirmDelete}
          >
            Excluir
          </Button>

        </DialogActions>

      </Dialog>

      {/* SNACKBAR */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={() => setOpenSnackbar(false)}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
      >

        <Alert
          severity="success"
          variant="filled"
          sx={{
            width: "100%",
          }}
        >
          Produto excluído com sucesso!
        </Alert>

      </Snackbar>

    </PageLayout>

  );
}

export default ProdutoList;