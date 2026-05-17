import { useForm, Controller } from "react-hook-form";

import InputMask from "react-input-mask";

import {
  TextField,
  Button,
  Box,
  Grid,
} from "@mui/material";

import { useNavigate } from "react-router-dom";

import PageLayout from "../components/common/PageLayout";

function ClienteForm() {

  const navigate = useNavigate();

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm();

  // =========================
  // SUBMIT
  // =========================

  const onSubmit = (data) => {
    console.log(data);
  };

  // =========================
  // CANCELAR
  // =========================

  const handleCancel = () => {
    navigate("/clientes");
  };

  // =========================
  // ESTILO PADRÃO DOS CAMPOS
  // =========================

  const inputStyle = {
    "& .MuiOutlinedInput-root": {

      "& fieldset": {
        transition: "0.2s",
      },

      "&.Mui-focused fieldset": {
        borderColor: "#f59e0b",
        borderWidth: 2,
      },
    },
  };

  return (

    <PageLayout title="Cadastro de Cliente">

      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
      >

        <Grid container spacing={2}>

          {/* NOME */}
          <Grid item xs={12} md={6}>

            <Controller
              name="nome"
              control={control}
              defaultValue=""
              rules={{
                required: "Nome obrigatório",

                maxLength: {
                  value: 100,
                  message: "Máximo 100 caracteres",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  autoFocus
                  label="Nome"
                  placeholder="Digite o nome do cliente"
                  title="Campo obrigatório"
                  error={!!errors.nome}
                  helperText={errors.nome?.message}
                  inputProps={{
                    maxLength: 100,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

          {/* EMAIL */}
          <Grid item xs={12} md={6}>

            <Controller
              name="email"
              control={control}
              defaultValue=""
              rules={{
                required: "E-mail obrigatório",

                pattern: {
                  value:
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/,

                  message: "E-mail inválido",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  type="email"
                  label="E-mail"
                  placeholder="cliente@email.com"
                  title="Digite um e-mail válido"
                  error={!!errors.email}
                  helperText={errors.email?.message}
                  inputProps={{
                    maxLength: 100,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

          {/* TELEFONE */}
          <Grid item xs={12} md={6}>

            <Controller
              name="telefone"
              control={control}
              defaultValue=""
              rules={{
                required: "Telefone obrigatório",
              }}
              render={({ field }) => (

                <InputMask
                  mask="(99) 99999-9999"
                  value={field.value}
                  onChange={field.onChange}
                >

                  {() => (
                    <TextField
                      fullWidth
                      label="Telefone"
                      placeholder="(49) 99999-9999"
                      title="Digite o telefone"
                      error={!!errors.telefone}
                      helperText={errors.telefone?.message}
                      inputProps={{
                        maxLength: 15,
                      }}
                      sx={inputStyle}
                    />
                  )}

                </InputMask>

              )}
            />

          </Grid>

          {/* CEP */}
          <Grid item xs={12} md={6}>

            <Controller
              name="cep"
              control={control}
              defaultValue=""
              rules={{
                required: "CEP obrigatório",
              }}
              render={({ field }) => (

                <InputMask
                  mask="99999-999"
                  value={field.value}
                  onChange={field.onChange}
                >

                  {() => (
                    <TextField
                      fullWidth
                      label="CEP"
                      placeholder="88500-000"
                      title="Digite o CEP"
                      error={!!errors.cep}
                      helperText={errors.cep?.message}
                      inputProps={{
                        maxLength: 9,
                      }}
                      sx={inputStyle}
                    />
                  )}

                </InputMask>

              )}
            />

          </Grid>

          {/* ENDEREÇO */}
          <Grid item xs={12}>

            <Controller
              name="endereco"
              control={control}
              defaultValue=""
              rules={{
                maxLength: {
                  value: 150,
                  message: "Máximo 150 caracteres",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Endereço"
                  placeholder="Rua, número, complemento"
                  title="Digite o endereço"
                  error={!!errors.endereco}
                  helperText={errors.endereco?.message}
                  inputProps={{
                    maxLength: 150,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

          {/* BAIRRO */}
          <Grid item xs={12} md={6}>

            <Controller
              name="bairro"
              control={control}
              defaultValue=""
              rules={{
                maxLength: {
                  value: 50,
                  message: "Máximo 50 caracteres",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Bairro"
                  placeholder="Digite o bairro"
                  title="Digite o bairro"
                  error={!!errors.bairro}
                  helperText={errors.bairro?.message}
                  inputProps={{
                    maxLength: 50,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

          {/* CIDADE */}
          <Grid item xs={12} md={6}>

            <Controller
              name="cidade"
              control={control}
              defaultValue=""
              rules={{
                maxLength: {
                  value: 50,
                  message: "Máximo 50 caracteres",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  label="Cidade"
                  placeholder="Digite a cidade"
                  title="Digite a cidade"
                  error={!!errors.cidade}
                  helperText={errors.cidade?.message}
                  inputProps={{
                    maxLength: 50,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

          {/* OBSERVAÇÃO */}
          <Grid item xs={12}>

            <Controller
              name="observacao"
              control={control}
              defaultValue=""
              rules={{
                maxLength: {
                  value: 200,
                  message: "Máximo 200 caracteres",
                },
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  fullWidth
                  multiline
                  rows={4}
                  label="Observação"
                  placeholder="Digite observações adicionais"
                  title="Observações"
                  error={!!errors.observacao}
                  helperText={errors.observacao?.message}
                  inputProps={{
                    maxLength: 200,
                  }}
                  sx={inputStyle}
                />
              )}
            />

          </Grid>

        </Grid>

        {/* BOTÕES */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "flex-end",
            gap: 2,
            mt: 4,
          }}
        >

          <Button
            variant="outlined"
            onClick={handleCancel}
          >
            Cancelar
          </Button>

          <Button
            type="submit"
            variant="contained"
          >
            Salvar
          </Button>

        </Box>

      </Box>

    </PageLayout>
  );
}

export default ClienteForm;