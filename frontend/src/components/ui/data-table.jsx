import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import LoadingState from "./loading-state";
import EmptyState from "./empty-state";

const DataTable = ({
  columns,
  rows,
  rowKey,
  renderRow,
  loading = false,
  emptyTitle = "Nenhum registro encontrado",
  emptyDescription,
  className,
}) => {
  if (loading) {
    return <LoadingState title="Carregando tabela" description="Aguarde enquanto os dados são carregados." className={className} />;
  }

  if (!rows?.length) {
    return <EmptyState title={emptyTitle} description={emptyDescription} className={className} />;
  }

  return (
    <div className={className}>
      <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
        <Table>
          <TableHeader className="bg-slate-50">
            <TableRow>
              {columns.map((column) => (
                <TableHead key={column.key} className={column.className}>
                  {column.label}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((row, index) => (
              <TableRow key={rowKey ? rowKey(row, index) : row.id || index} className="hover:bg-slate-50/70">
                {renderRow(row, index)}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default DataTable;
