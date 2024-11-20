import { BaseSyntheticEvent, useState } from "react";
import { useFormik } from "formik";
import louieService from "./services/louie";
import Markdown from "react-markdown";
import { Box, FormControl, Container } from "@mui/material";

const App = () => {
  const [summaryResponse, setSummaryResponse] = useState("No content");

  const formik = useFormik({
    initialValues: {
      fileParam: "",
    },

    onSubmit: async (values) => {
      console.log("logging values from onSubmit ", values);

      const result: string = await louieService.getSummary(values);
      setSummaryResponse(result);
      console.log("response from fastapi server");
      console.log(result);
    },
  });

  const onChange = (event: BaseSyntheticEvent) => {
    const file = event.target.files[0];
    formik.setFieldValue("fileParam", file);
    const reader = new FileReader();

    // temporarily show file contentx
    reader.onload = (e) => {
      // The file's text will be printed here
      const result = e.target?.result;

      return result;
    };

    //shows the files values properly
    reader.readAsText(file);
  };

  /*const initialValues: SummaryFormValues = {
    fileParam: "",
    questionParam: "",
  };*/

  return (
    <>
      <Container>
        <h3>Extractive summarizer</h3>
        <Box component="section" sx={{ p: 2, border: "1px dashed grey" }}>
          <form onSubmit={formik.handleSubmit}>
            <FormControl variant="standard">
              <Box>Input file:</Box>
              <input
                id="fileParam"
                name="test"
                type="file"
                onChange={onChange}
              ></input>

              <div>
                <button type="submit">Submit</button>
              </div>
            </FormControl>
          </form>
        </Box>
        <Box component="section" sx={{ p: 2, border: "1px dashed grey" }}>
          <Markdown>{summaryResponse}</Markdown>
        </Box>
      </Container>
    </>
  );
};

export default App;
