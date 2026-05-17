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

function ClienteList() {

  const navigate = useNavigate();

  const clientes = [
    {
      id: 1,
      nome: 'Carlos Mendes',
      cpf: '111.222.333-44',
      telefone: '(49) 99999-3333'
    },
    {
      id: 2,
      nome: 'Ana Oliveira',
      cpf: '555.666.777-88',
      telefone: '(49) 99999-4444'
    }
  ];

  const actions = (
    <Button
      variant="contained"
      color="primary"
      onClick={() => navigate('/cliente')}
      startIcon={<FiberNew />}
    >
      Novo
    </Button>
  );

  const handleView = (cliente) =>
    console.log(cliente);

  const handleEdit = (cliente) =>
    navigate(`/cliente/${cliente.id}`);

  const handleDelete = (cliente) =>
    console.log(cliente);

  const renderDesktopRow = (cliente) => (
    <TableRow key={cliente.id} hover>

      <TableCell>{cliente.id}</TableCell>

      <TableCell sx={{ fontWeight: 500 }}>
        {cliente.nome}
      </TableCell>

      <TableCell>{cliente.cpf}</TableCell>

      <TableCell>{cliente.telefone}</TableCell>

      <TableCell>
        <ActionButtons
          item={cliente}
          onView={handleView}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </TableCell>

    </TableRow>
  );

  const renderMobileCard = (cliente) => (
    <Card key={cliente.id} sx={{ mb: 2 }}>
      <CardContent>

        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          {cliente.nome}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Typography variant="body2">
          <strong>CPF:</strong> {cliente.cpf}
        </Typography>

        <Typography variant="body2">
          <strong>Telefone:</strong> {cliente.telefone}
        </Typography>

        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            mt: 2
          }}
        >
          <ActionButtons
            item={cliente}
            onView={handleView}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </Box>

      </CardContent>
    </Card>
  );

  return (
    <PageLayout title="Clientes" actions={actions}>

      <Box sx={{ display: { xs: 'none', md: 'block' } }}>
        <TableContainer component={Paper}>
          <Table>

            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Nome</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>CPF</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Telefone</TableCell>
                <TableCell sx={{ fontWeight: 600 }}>Ações</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {clientes.map((cliente) =>
                renderDesktopRow(cliente)
              )}
            </TableBody>

          </Table>
        </TableContainer>
      </Box>

      <Box sx={{ display: { xs: 'block', md: 'none' } }}>
        {clientes.map((cliente) =>
          renderMobileCard(cliente)
        )}
      </Box>

    </PageLayout>
  );
}

export default ClienteList;