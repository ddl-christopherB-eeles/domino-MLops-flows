# setup.sh
unlink /workflow/inputs
unlink /workflow/outputs
rm -rf /workflow/inputs
rm -rf /workflow/outputs
ln -s /workflow/data /workflow/inputs
ln -s /workflow/data /workflow/outputs