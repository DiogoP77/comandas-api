import {
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
} from '@mui/material';

import { FiberNew } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

import PageLayout from "../components/common/PageLayout";
import ActionButtons from "../components/common/ActionButtons";

function FuncionarioList() {

  const navigate = useNavigate();

  const funcionarios = [
    {
      id: 1,
      nome: 'João Silva',
      cpf: '123.456.789-00',
      cargo: 'Garçom',
      telefone: '(49) 99999-1111'
    },
    {
      id: 2,
      nome: 'Maria Souza',
      cpf: '987.654.321-00',
      cargo: 'Caixa',
      telefone: '(49) 99999-2222'
    }
  ];

  const actions = (
    <Button
      variant="contained"
      color="primary"
      onClick={() => navigate('/funcionario')}
      startIcon={<FiberNew />}
      sx={{ fontWeight: 600, px: 2, py: 1 }}
    >
      Novo
    </Button>
  );

  const handleView = (funcionario) =>
    console.log("Visualizar funcionário:", funcionario);

  const handleEdit = (funcionario) =>
    navigate(`/funcionario/${funcionario.id}`);

  const handleDelete = (funcionario) =>
    console.log("Excluir funcionário:", funcionario);

  const columns = [
    { field: 'id', headerName: 'ID' },
    { field: 'nome', headerName: 'Nome' },
    { field: 'cpf', headerName: 'CPF' },
    { field: 'cargo', headerName: 'Cargo' },
    { field: 'telefone', headerName: 'Telefone' },
    {
      field: 'actions',
      headerName: 'Ações'
    }
  ];

  const renderDesktopRow = (funcionario) => (
    <TableRow key={funcionario.id} hover>

      <TableCell>{funcionario.id}</TableCell>

      <TableCell sx={{ fontWeight: 500 }}>
        {funcionario.nome}
      </TableCell>

      <TableCell>{funcionario.cpf}</TableCell>

      <TableCell>{funcionario.cargo}</TableCell>

      <TableCell>{funcionario.telefone}</TableCell>

      <TableCell>
        <ActionButtons
          item={funcionario}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </TableCell>

    </TableRow>
  );

  const renderMobileCard = (funcionario) => (
    <Card key={funcionario.id} sx={{ mb: 2 }}>
      <CardContent>

        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          {funcionario.nome}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography variant="body2">
          <strong>CPF:</strong> {funcionario.cpf}
        </Typography>

        <Typography variant="body2">
          <strong>Cargo:</strong> {funcionario.cargo}
        </Typography>

        <Typography variant="body2">
          <strong>Telefone:</strong> {funcionario.telefone}
        </Typography>

        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            mt: 2
          }}
        >
          <ActionButtons
            item={funcionario}
            onView={handleView}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </Box>

      </CardContent>
    </Card>
  );

  return (
    <PageLayout title="Funcionários" actions={actions}>

      {/* Desktop */}
      <Box sx={{ display: { xs: 'none', md: 'block' } }}>
        <TableContainer component={Paper}>
          <Table>

            <TableHead>
              <TableRow>
                {columns.map((column, index) => (
                  <TableCell
                    key={index}
                    sx={{ fontWeight: 600 }}
                  >
                    {column.headerName}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>

            <TableBody>
              {funcionarios.map((funcionario) =>
                renderDesktopRow(funcionario)
              )}
            </TableBody>

          </Table>
        </TableContainer>
      </Box>

      {/* Mobile */}
      <Box sx={{ display: { xs: 'block', md: 'none' } }}>
        {funcionarios.map((funcionario) =>
          renderMobileCard(funcionario)
        )}
      </Box>

    </PageLayout>
  );
}

export default FuncionarioList;