import { useForm, Controller } from 'react-hook-form';

import {
  TextField,
  Button,
  Box
} from '@mui/material';

import { useNavigate } from 'react-router-dom';

import PageLayout from "../components/common/PageLayout";
import { useValidationRules } from '../hooks/useValidationRules';

const FuncionarioForm = () => {

  const {
    control,
    handleSubmit,
    formState: { errors }
  } = useForm();

  const validationRules = useValidationRules();

  const navigate = useNavigate();

  const onSubmit = (data) => {
    console.log("Dados do funcionário:", data);
  };

  const handleCancel = () => {
    navigate('/funcionarios');
  };

  return (
    <PageLayout title="Dados Funcionário">

      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
      >

        <Controller
          name="nome"
          control={control}
          defaultValue=""
          rules={validationRules.nome}
          render={({ field }) => (
            <TextField
              {...field}
              label="Nome"
              fullWidth
              margin="normal"
              error={!!errors.nome}
              helperText={errors.nome?.message}
            />
          )}
        />

        <Controller
          name="cpf"
          control={control}
          defaultValue=""
          rules={validationRules.cpf}
          render={({ field }) => (
            <TextField
              {...field}
              label="CPF"
              fullWidth
              margin="normal"
              error={!!errors.cpf}
              helperText={errors.cpf?.message}
            />
          )}
        />

        <Controller
          name="cargo"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              label="Cargo"
              fullWidth
              margin="normal"
            />
          )}
        />

        <Controller
          name="telefone"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              label="Telefone"
              fullWidth
              margin="normal"
            />
          )}
        />

        <Box
          sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            mt: 3
          }}
        >
          <Button
            sx={{ mr: 1 }}
            onClick={handleCancel}
          >
            Cancelar
          </Button>

          <Button
            type="submit"
            variant="contained"
          >
            Cadastrar
          </Button>
        </Box>

      </Box>
    </PageLayout>
  );
};

export default FuncionarioForm;