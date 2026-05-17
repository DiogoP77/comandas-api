import { Box, IconButton, Tooltip } from "@mui/material";

import {
  Edit,
  Delete,
  Visibility
} from "@mui/icons-material";

const ActionButtons = ({
  item,
  onView,
  onEdit,
  onDelete
}) => {
  const handleDelete = () => {
    const confirmDelete = window.confirm(
      `Deseja excluir "${item.nome}" ?`
    );

    if (confirmDelete) {
      onDelete(item);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        gap: 1,
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      {/* VISUALIZAR */}
      <Tooltip title="Visualizar" arrow>
        <IconButton
          size="small"
          color="primary"
          onClick={() => onView(item)}
          sx={{
            width: 40,
            height: 40,
            border: "1px solid",
            borderColor: "primary.main",

            "&:hover": {
              backgroundColor: "primary.main",
              color: "white",
              transform: "scale(1.05)"
            },

            transition: "0.2s"
          }}
        >
          <Visibility fontSize="small" />
        </IconButton>
      </Tooltip>

      {/* EDITAR */}
      <Tooltip title="Editar" arrow>
        <IconButton
          size="small"
          color="secondary"
          onClick={() => onEdit(item)}
          sx={{
            width: 40,
            height: 40,
            border: "1px solid",
            borderColor: "secondary.main",

            "&:hover": {
              backgroundColor: "secondary.main",
              color: "white",
              transform: "scale(1.05)"
            },

            transition: "0.2s"
          }}
        >
          <Edit fontSize="small" />
        </IconButton>
      </Tooltip>

      {/* EXCLUIR */}
      <Tooltip title="Excluir" arrow>
        <IconButton
          size="small"
          color="error"
          onClick={handleDelete}
          sx={{
            width: 40,
            height: 40,
            border: "1px solid",
            borderColor: "error.main",

            "&:hover": {
              backgroundColor: "error.main",
              color: "white",
              transform: "scale(1.05)"
            },

            transition: "0.2s"
          }}
        >
          <Delete fontSize="small" />
        </IconButton>
      </Tooltip>
    </Box>
  );
};

export default ActionButtons;