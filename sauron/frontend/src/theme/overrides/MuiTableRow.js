import palette from "../palette";

const tableRow = {
  root: {
    "&$selected": {
      backgroundColor: palette.background.default,
    },
    "&$hover": {
      "&:hover": {
        backgroundColor: palette.primary.action,
      },
    },
  },
};

export default tableRow;
