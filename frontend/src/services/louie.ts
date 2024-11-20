import axios from "axios";
import { SummaryFormValues } from "../types";
import { apiBaseUrl } from "../constants";

const getSummary = async (formValues: SummaryFormValues) => {
  console.log("formValues");
  console.log(formValues);
  const { data } = await axios.post(`${apiBaseUrl}`, formValues, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return data;
};

export default {
  getSummary,
};
